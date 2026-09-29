"""
python manage.py seed [--reset] [--no-demo]

Loads the Holidaybank catalogue, content and (by default) demo operations data.
Safe to re-run: every record is upserted by a natural key (slug, name, email,
URL), so running it twice changes nothing. Site settings are only written on
first run or with --reset, so edits made in the dashboard survive a re-seed.

--reset    delete catalogue, content and enquiries first, and restore settings
           to their defaults. Accounts are kept.
--no-demo  skip demo tours, testimonials, blog posts, staff and enquiries,
           loading only content taken from the original website.
"""
import copy
import os
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import AdminUser, AuditLog, Role
from apps.accounts.permissions_catalog import SYSTEM_ROLES
from apps.catalog.models import Country, Destination, Place, Tour, TourCategory, TourImage, TravelArea
from apps.content.defaults import SITE_SETTINGS_DEFAULTS
from apps.content.models import BlogPost, Faq, Service, SiteSettings, Tag, Testimonial
from apps.enquiries.models import Enquiry, EnquiryEvent, EnquiryReferenceCounter
from apps.enquiries.services import create_with_reference, describe_status_change, log_event
from apps.media.models import ImageAsset

from ...data import catalog as catalog_data
from ...data import content as content_data
from ...data.images import IMAGES


class Command(BaseCommand):
    help = 'Load Holidaybank Expeditions seed data (idempotent).'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Wipe content and enquiries first.')
        parser.add_argument('--no-demo', action='store_true', help='Skip demo/sample records.')

    def handle(self, *args, reset=False, no_demo=False, **options):
        demo = not no_demo
        with transaction.atomic():
            if reset:
                self._reset()
            roles = self._roles()
            admin = self._admin(roles)
            self._images()
            self._countries()
            self._categories()
            self._destinations()
            self._tours(demo)
            self._areas()
            self._services()
            self._faqs()
            self._settings(reset)
            if demo:
                self._testimonials()
                self._blog()
                staff = self._staff(roles)
                self._enquiries(staff, admin)
                self._audit(admin, staff)
        self._summary()

    # ------------------------------------------------------------------

    def log(self, message):
        self.stdout.write(f'  {message}')

    def _reset(self):
        self.stdout.write(self.style.WARNING('Resetting content and enquiries...'))
        EnquiryEvent.objects.all().delete()
        Enquiry.objects.all().delete()
        EnquiryReferenceCounter.objects.all().delete()
        Testimonial.objects.all().delete()
        TourImage.objects.all().delete()
        Tour.objects.all().delete()
        TravelArea.objects.filter(parent__isnull=False).delete()
        TravelArea.objects.all().delete()
        Place.objects.all().delete()
        Destination.objects.all().delete()
        TourCategory.objects.filter(parent__isnull=False).delete()
        TourCategory.objects.all().delete()
        Country.objects.all().delete()
        BlogPost.objects.all().delete()
        Tag.objects.all().delete()
        Faq.objects.all().delete()
        Service.objects.all().delete()
        SiteSettings.objects.all().delete()
        ImageAsset.objects.filter(file='').delete()
        ImageAsset.objects.filter(file__isnull=True).delete()
        AdminUser.objects.filter(is_sample=True).delete()

    def _roles(self) -> dict:
        roles = {}
        for spec in SYSTEM_ROLES:
            role, created = Role.objects.get_or_create(
                name=spec['name'],
                defaults={'description': spec['description'], 'permissions': spec['permissions'], 'locked': spec['locked']},
            )
            if role.locked:
                # The locked role always tracks the full permission list.
                role.permissions = spec['permissions']
                role.save(update_fields=['permissions'])
            roles[role.name] = role
        self.log(f'{len(roles)} roles')
        return roles

    def _admin(self, roles) -> AdminUser | None:
        email = (os.environ.get('ADMIN_EMAIL') or 'admin@holidaybankexpeditions.com').strip().lower()
        password = os.environ.get('ADMIN_PASSWORD') or ''
        existing = AdminUser.objects.filter(email=email).first()
        if existing:
            self.log(f'administrator {email} already exists (password unchanged)')
            return existing
        if len(password) < 12:
            self.stdout.write(self.style.WARNING(
                '  ADMIN_PASSWORD is not set (or shorter than 12 characters); no administrator created. '
                'Set it in .env and re-run, or use `python manage.py createsuperuser`.'
            ))
            return None
        admin = AdminUser.objects.create_superuser(
            email=email, password=password, name=os.environ.get('ADMIN_NAME') or 'Administrator', role=roles['Administrator']
        )
        self.log(f'administrator {email} created')
        return admin

    def _images(self):
        for row in IMAGES:
            ImageAsset.objects.update_or_create(
                url=f"/images/{row['file']}",
                defaults={
                    'alt': row['alt'],
                    'title': row['file'].rsplit('.', 1)[0].replace('-', ' '),
                    'source': row['source'],
                    'photographer': row['photographer'],
                    'pexels_id': row['pexels_id'],
                    'source_url': f"https://www.pexels.com/photo/{row['pexels_id']}/" if row['pexels_id'] else '',
                    'license': row['license'],
                    'notes': row['notes'],
                    'width': row['width'],
                    'height': row['height'],
                },
            )
        for name, alt in [
            ('logo.svg', 'Holidaybank Expeditions: Travel in Style'),
            ('logo-on-light.svg', 'Holidaybank Expeditions: Travel in Style'),
            ('logo-compact.svg', 'Holidaybank Expeditions'),
            ('logo-mark.svg', 'Holidaybank Expeditions'),
        ]:
            ImageAsset.objects.update_or_create(
                url=f'/brand/{name}',
                defaults={
                    'alt': alt, 'title': name, 'source': ImageAsset.Source.ORIGINAL, 'tags': ['brand'],
                    'license': 'Holidaybank Expeditions logo',
                    'notes': 'Vector redraw of the original logo bitmap.',
                },
            )
        self.log(f'{len(IMAGES) + 4} images registered')

    @staticmethod
    def _img(file):
        if not file:
            return None
        return ImageAsset.objects.get(url=f'/images/{file}')

    def _countries(self):
        for row in catalog_data.COUNTRIES:
            Country.objects.update_or_create(slug=row['slug'], defaults=row)
        self.log(f'{len(catalog_data.COUNTRIES)} countries')

    def _categories(self):
        for row in catalog_data.CATEGORIES:
            parent = TourCategory.objects.get(slug=row['parent']) if row.get('parent') else None
            TourCategory.objects.update_or_create(
                slug=row['slug'],
                defaults={
                    'name': row['name'], 'parent': parent, 'kind': row['kind'], 'order': row['order'],
                    'eyebrow': row['eyebrow'], 'nav_label': row['nav_label'], 'description': row['description'],
                    'hero_image': self._img(row['image']), 'status': 'published',
                    'source_note': 'Name and description from the original website navigation.',
                },
            )
        self.log(f'{len(catalog_data.CATEGORIES)} categories')

    def _destinations(self):
        for row in catalog_data.DESTINATIONS:
            dest, _ = Destination.objects.update_or_create(
                slug=row['slug'],
                defaults={
                    'name': row['name'], 'country': Country.objects.get(name=row['country']), 'tagline': row['tagline'],
                    'category_label': row['category_label'], 'overview': row['overview'],
                    'hero_image': self._img(row['hero']), 'card_image': self._img(row['card']),
                    'highlights': row['highlights'], 'best_time': row['best_time'], 'featured': row.get('featured', False),
                    'order': row['order'], 'status': 'published', 'source_note': catalog_data.DESTINATION_NOTE,
                },
            )
            dest.places.all().delete()
            for index, place in enumerate(row['places']):
                from apps.common.slugs import slugify

                Place.objects.create(
                    destination=dest, name=place['name'], slug=slugify(place['name']), kind=place['kind'],
                    blurb=place['blurb'], image=self._img(place['image']), best_time=place['best_time'],
                    highlights=place['highlights'], order=index,
                )
        self.log(f'{len(catalog_data.DESTINATIONS)} destinations with places')

    def _tours(self, demo):
        from apps.common.slugs import slugify

        count = 0
        for row in catalog_data.TOURS:
            sample = row.get('sample', False)
            if sample and not demo:
                continue
            tour, _ = Tour.objects.update_or_create(
                slug=slugify(row['title']),
                defaults={
                    'title': row['title'], 'category': TourCategory.objects.get(slug=row['category']),
                    'summary': row['summary'], 'description': row['description'],
                    'price_from': row['price_from'], 'currency': row['currency'], 'price_basis': 'per person',
                    'duration_days': row['days'], 'duration_nights': row['nights'],
                    'group_size_max': row.get('group_size_max', 12), 'difficulty': row.get('difficulty', 'easy'),
                    'rating': 0, 'review_count': 0,
                    'destination': Destination.objects.filter(slug=row['destination']).first() if row.get('destination') else None,
                    'location_label': row.get('location_label', ''),
                    'highlights': row['highlights'], 'inclusions': row['inclusions'], 'exclusions': row['exclusions'],
                    'itinerary': row['itinerary'], 'hero_image': self._img(row['image']),
                    'featured': row.get('featured', False), 'best_selling': row.get('best_selling', False),
                    'order': row.get('order', 0), 'status': 'published',
                    'parks': row.get('parks', []), 'game_drive_count': row.get('game_drive_count'),
                    'conservancy_fees_included': row.get('conservancy_fees_included'),
                    'departs_from': row.get('departs_from', ''), 'visa_support': row.get('visa_support'),
                    'is_sample': sample,
                    'source_note': catalog_data.SAMPLE_NOTE if sample else catalog_data.ORIGINAL_NOTE,
                },
            )
            tour.countries.set(Country.objects.filter(name__in=row['countries']))
            TourImage.objects.filter(tour=tour).delete()
            for index, file in enumerate(row.get('gallery', [])):
                TourImage.objects.create(tour=tour, image=self._img(file), order=index)
            count += 1
        self.log(f'{count} tours')

    def _areas(self):
        note = 'Regional grouping for the homepage packages section.'
        count = 0
        for group_row in catalog_data.AREAS:
            group, _ = TravelArea.objects.update_or_create(
                slug=group_row['slug'],
                defaults={'name': group_row['name'], 'parent': None, 'order': group_row['order'],
                          'status': 'published', 'source_note': note},
            )
            for index, (slug, name) in enumerate(group_row['areas']):
                details = catalog_data.AREA_DETAILS.get(slug, {})
                area, _ = TravelArea.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': name, 'parent': group, 'order': index, 'status': 'published', 'source_note': note,
                        'tag': details.get('tag', ''), 'description': details.get('description', ''),
                        'image': self._img(details.get('image')),
                    },
                )
                # Places are recreated with their destination on every run, so relink each time.
                area.places.set(Place.objects.filter(destination__slug='kenya', name__in=details.get('places', [])))
                count += 1

        # Inverted so each tour's set is written once, and a re-run changes nothing.
        by_tour: dict = {}
        for slug, titles in catalog_data.AREA_TOURS.items():
            for title in titles:
                by_tour.setdefault(title, []).append(slug)
        for tour in Tour.objects.filter(title__in=by_tour):
            tour.areas.set(TravelArea.objects.filter(slug__in=by_tour[tour.title]))
        self.log(f'{len(catalog_data.AREAS)} area groups, {count} areas')

    def _services(self):
        from apps.common.slugs import slugify

        for row in content_data.SERVICES:
            Service.objects.update_or_create(
                slug=slugify(row['title']),
                defaults={
                    'title': row['title'], 'summary': row['summary'], 'body': row['body'], 'icon': row['icon'],
                    'image': self._img(row['image']), 'highlights': row['highlights'],
                    'cta_label': row['cta'][0], 'cta_href': row['cta'][1], 'order': row['order'], 'status': 'published',
                    'source_note': 'Restates services described on the original website.',
                },
            )
        self.log(f'{len(content_data.SERVICES)} services')

    def _faqs(self):
        for index, (group, question, answer) in enumerate(content_data.FAQS):
            Faq.objects.update_or_create(
                question=question,
                defaults={'answer': answer, 'group': group, 'order': index, 'status': 'published', 'is_sample': True,
                          'source_note': 'Drafted for this build; confirm the answer reflects actual policy.'},
            )
        self.log(f'{len(content_data.FAQS)} FAQs')

    def _settings(self, reset):
        row = SiteSettings.objects.filter(key='primary').first()
        if row and not reset:
            self.log('site settings kept (already customised or seeded)')
            return
        values = {attr: copy.deepcopy(SITE_SETTINGS_DEFAULTS.get(wire, {})) for wire, attr in SiteSettings.SECTIONS.items()}
        SiteSettings.objects.update_or_create(key='primary', defaults=values)
        self.log('site settings written from defaults')

    def _testimonials(self):
        for index, (name, location, tour_title, rating, quote) in enumerate(content_data.TESTIMONIALS):
            Testimonial.objects.update_or_create(
                author_name=name,
                quote=quote,
                defaults={
                    'author_location': location, 'tour': Tour.objects.filter(title=tour_title).first(),
                    'tour_name': tour_title, 'rating': rating, 'featured': index < 4, 'order': index,
                    'status': 'published', 'is_sample': True,
                    'source_note': 'Demo review for layout only. Replace with genuine customer reviews before launch.',
                },
            )
        self.log(f'{len(content_data.TESTIMONIALS)} demo testimonials')

    def _blog(self):
        from apps.common.slugs import slugify

        now = timezone.now()
        for row in content_data.BLOG_POSTS:
            post, _ = BlogPost.objects.update_or_create(
                slug=slugify(row['title']),
                defaults={
                    'title': row['title'], 'excerpt': row['excerpt'], 'content': row['content'],
                    'cover_image': self._img(row['image']), 'author_name': 'Holidaybank Expeditions',
                    'reading_minutes': max(2, round(len(row['content'].split()) / 220)),
                    'published_at': now - timedelta(days=row['days_ago']), 'featured': row.get('featured', False),
                    'status': 'published', 'is_sample': True,
                    'source_note': 'Demo article written for this build.',
                },
            )
            post.tags.set([Tag.objects.get_or_create(name=t)[0] for t in row['tags']])
        self.log(f'{len(content_data.BLOG_POSTS)} demo blog posts')

    def _staff(self, roles) -> list[AdminUser]:
        staff = []
        for row in content_data.STAFF:
            user = AdminUser.objects.filter(email=row['email']).first()
            if user is None:
                user = AdminUser.objects.create_user(email=row['email'], name=row['name'], role=roles[row['role']], is_sample=True)
            staff.append(user)
        self.log(f'{len(staff)} demo staff (cannot sign in)')
        return staff

    def _enquiries(self, staff, admin):
        if Enquiry.objects.filter(is_sample=True).exists():
            self.log('demo enquiries already present')
            return
        now = timezone.now()
        consultants = staff[:2]
        for row in content_data.ENQUIRIES:
            created = now - timedelta(days=row['days_ago'], hours=3)
            tour = Tour.objects.filter(title=row.get('tour')).first() if row.get('tour') else None
            assignee = consultants[row['assignee']] if 'assignee' in row else None
            enquiry = create_with_reference(
                created_at=created,
                type=row['type'], name=row['name'], email=row['email'], phone=row.get('phone', ''),
                interest=row.get('interest', ''), budget=row.get('budget'), budget_currency=row.get('budget_currency', ''),
                message=row.get('message', ''), tour=tour, tour_title=tour.title if tour else '',
                travel_date=(now + timedelta(days=row['travel_in_days'])).date() if row.get('travel_in_days') else None,
                guests=row.get('guests'), status=row['status'], assignee=assignee,
                assigned_at=created + timedelta(hours=2) if assignee else None,
                last_contacted_at=created + timedelta(days=1) if row['status'] in ('in_progress', 'quoted', 'won', 'lost') else None,
                follow_up_at=now + timedelta(days=row['follow_up_in_days']) if 'follow_up_in_days' in row else None,
                closed_at=created + timedelta(days=6) if row['status'] in ('won', 'lost') else None,
                is_sample=True,
                source='website',
            )
            summary = (f'Booking enquiry received for {enquiry.tour_title}' if enquiry.type == 'booking'
                       else 'Contact enquiry received')
            self._event(enquiry, 'created', summary, created, None, meta={'source': 'website'})
            if assignee:
                actor = {'actor': assignee, 'actor_name': assignee.name}
                self._event(enquiry, 'assigned', f'{assignee.name} claimed this enquiry', created + timedelta(hours=2), actor)
                path = ['assigned', 'in_progress', 'quoted', row['status']]
                previous = 'new'
                for step, status in enumerate(path[: path.index(row['status']) + 1] if row['status'] in path else path):
                    if status == previous:
                        continue
                    when = created + timedelta(hours=2 + step * 20)
                    self._event(enquiry, 'status_change', describe_status_change(previous, status), when, actor,
                                meta={'from': previous, 'to': status})
                    if status == 'in_progress':
                        self._event(enquiry, 'contacted', f'{assignee.name} contacted the customer', when, actor,
                                    note='Called to confirm dates and group size.')
                    previous = status
        self.log(f'{len(content_data.ENQUIRIES)} demo enquiries with timelines')

    @staticmethod
    def _event(enquiry, type_, summary, when, actor, note=None, meta=None):
        event = log_event(enquiry, type_, summary, actor=actor, note=note, meta=meta)
        EnquiryEvent.objects.filter(pk=event.pk).update(created_at=min(when, timezone.now()))

    def _audit(self, admin, staff):
        if AuditLog.objects.exists():
            return
        actor_email = admin.email if admin else 'system'
        for user in staff:
            entry = AuditLog.objects.create(
                actor=admin, actor_email=actor_email, action='user.create', target_type='user',
                target_id=user.id, target_label=user.email,
                changes={'after': {'name': user.name, 'email': user.email, 'role': user.role.name if user.role else None}},
                ip='127.0.0.1',
            )
            AuditLog.objects.filter(pk=entry.pk).update(created_at=timezone.now() - timedelta(days=40))
        self.log('audit log entries for demo staff')

    def _summary(self):
        self.stdout.write(self.style.SUCCESS(
            'Seed complete: '
            f'{Tour.objects.count()} tours ({Tour.objects.filter(is_sample=True).count()} demo), '
            f'{Destination.objects.count()} destinations, {Place.objects.count()} places, '
            f'{ImageAsset.objects.count()} images, {Enquiry.objects.count()} enquiries, '
            f'{Testimonial.objects.count()} testimonials, {BlogPost.objects.count()} posts, '
            f'{Faq.objects.count()} FAQs, {Service.objects.count()} services.'
        ))
