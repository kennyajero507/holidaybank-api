"""
End-to-end tests of the HTTP API against the seeded catalogue.

Run:  python manage.py test tests
"""
import io
import os
import shutil
import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from apps.accounts.models import AdminUser, AuditLog, Role
from apps.catalog.models import Tour
from apps.enquiries.models import Enquiry

ORIGIN = 'http://localhost:3000'
PASSWORD = 'correct-horse-battery-staple'


class ApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        os.environ['ADMIN_EMAIL'] = 'admin@test.example'
        os.environ['ADMIN_PASSWORD'] = PASSWORD
        call_command('seed', stdout=io.StringIO())
        cls.admin = AdminUser.objects.get(email='admin@test.example')

    def setUp(self):
        self.client = APIClient(HTTP_ORIGIN=ORIGIN)

    def login(self, email='admin@test.example', password=PASSWORD):
        res = self.client.post('/api/auth/login', {'email': email, 'password': password}, format='json')
        self.assertEqual(res.status_code, 200, res.content)
        return res

    def make_user(self, role_name, email):
        user = AdminUser(email=email, name=role_name, role=Role.objects.get(name=role_name))
        user.set_password(PASSWORD)
        user.save()
        return user


class PublicCatalogueTests(ApiTestCase):
    def test_health(self):
        body = self.client.get('/api/health').json()
        self.assertEqual(body['data']['database'], 'connected')

    def test_tour_list_envelope_and_pagination(self):
        body = self.client.get('/api/tours?limit=5').json()
        self.assertTrue(body['success'])
        self.assertEqual(len(body['data']), 5)
        self.assertEqual(body['meta']['total'], 24)
        self.assertTrue(body['meta']['hasNextPage'])
        tour = body['data'][0]
        for key in ('_id', 'slug', 'durationLabel', 'categoryInfo', 'heroImage', 'countries', 'priceFrom', 'isSample'):
            self.assertIn(key, tour)
        self.assertIsInstance(tour['priceFrom'], float)

    def test_category_group_includes_children(self):
        safaris = self.client.get('/api/tours?category=safaris&limit=100').json()['meta']['total']
        kenyan = self.client.get('/api/tours?category=kenyan-safaris&limit=100').json()['meta']['total']
        east = self.client.get('/api/tours?category=east-africa-safaris&limit=100').json()['meta']['total']
        self.assertEqual(safaris, kenyan + east)
        self.assertEqual(self.client.get('/api/tours?category=nope').json()['meta']['total'], 0)

    def test_original_packages_preserved(self):
        body = self.client.get('/api/tours/diani-beach-escape').json()['data']
        self.assertEqual(body['priceFrom'], 24500)
        self.assertEqual(body['currency'], 'KES')
        self.assertEqual(body['locationLabel'], 'Diani, Coast')
        self.assertFalse(body['isSample'])
        self.assertEqual(body['reviewCount'], 0)

    def test_filters(self):
        kenya = self.client.get('/api/tours?country=Kenya&limit=100').json()['data']
        self.assertTrue(all('Kenya' in t['countries'] for t in kenya))
        europe = self.client.get('/api/tours?region=europe&limit=100').json()['data']
        self.assertTrue(europe and all(t['currency'] == 'USD' for t in europe))
        q = self.client.get('/api/tours?q=gorilla').json()['data']
        self.assertTrue(any('Gorilla' in t['title'] for t in q))

    def test_related_and_404(self):
        related = self.client.get('/api/tours/maasai-mara-3-days/related').json()['data']
        self.assertTrue(1 <= len(related) <= 3)
        res = self.client.get('/api/tours/does-not-exist')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()['error']['code'], 'NOT_FOUND')

    def test_drafts_are_hidden(self):
        Tour.objects.filter(slug='paris-city-break').update(status='draft')
        self.assertEqual(self.client.get('/api/tours/paris-city-break').status_code, 404)

    def test_destinations_and_places(self):
        body = self.client.get('/api/destinations/kenya').json()['data']
        self.assertEqual(body['country'], 'Kenya')
        self.assertGreaterEqual(body['parkCount'], 5)
        self.assertIn('url', body['parks'][0]['image'])

    def test_category_tree(self):
        tree = self.client.get('/api/categories').json()['data']
        self.assertEqual([c['slug'] for c in tree], ['kenyan-packages', 'international', 'safaris'])
        safaris = tree[2]
        self.assertEqual(len(safaris['children']), 2)
        self.assertEqual(safaris['tourCount'], sum(c['tourCount'] for c in safaris['children']))

    def test_settings_and_media_credits(self):
        settings = self.client.get('/api/settings').json()['data']
        self.assertEqual(settings['hero']['title'], "Discover East Africa's Wild Beauty")
        self.assertEqual(len(settings['heroSlides']), 9)
        self.assertTrue(settings['notice']['enabled'])
        media = self.client.get('/api/media?source=pexels&limit=100').json()
        self.assertTrue(all(m['sourceUrl'].startswith('https://www.pexels.com/photo/') for m in media['data']))

    def test_invalid_query_is_422(self):
        res = self.client.get('/api/tours?limit=1000')
        self.assertEqual(res.status_code, 422)
        self.assertIn('limit', res.json()['error']['details'])


class EnquirySubmissionTests(ApiTestCase):
    def test_contact_enquiry(self):
        res = self.client.post('/api/enquiries', {
            'type': 'contact', 'name': 'Test Person', 'email': 'TEST@example.com',
            'interest': 'Kenyan Packages', 'budget': 40000, 'budgetCurrency': 'KES',
            'message': 'A weekend for two in October please.',
        }, format='json')
        self.assertEqual(res.status_code, 201, res.content)
        data = res.json()['data']
        self.assertRegex(data['reference'], r'^ENQ-\d{4}-\d{4}$')
        self.assertNotIn('adminNotes', data)
        enquiry = Enquiry.objects.get(pk=data['id'])
        self.assertEqual(enquiry.email, 'test@example.com')
        self.assertEqual(enquiry.events.first().type, 'created')

    def test_booking_enquiry_links_tour(self):
        tour = Tour.objects.get(slug='maasai-mara-3-days')
        res = self.client.post('/api/enquiries', {
            'type': 'booking', 'name': 'Booker', 'email': 'b@example.com', 'tour': str(tour.id),
            'guests': {'adults': 2, 'children': 1, 'infants': 0},
        }, format='json')
        self.assertEqual(res.status_code, 201, res.content)
        self.assertEqual(Enquiry.objects.get(pk=res.json()['data']['id']).tour_title, tour.title)

    def test_references_are_sequential(self):
        refs = []
        for i in range(3):
            res = self.client.post('/api/enquiries', {'type': 'contact', 'name': f'P{i}x', 'email': f'p{i}@example.com',
                                                      'message': 'Tell me about safaris please.'}, format='json')
            refs.append(res.json()['data']['reference'])
        seqs = [int(r.rsplit('-', 1)[1]) for r in refs]
        self.assertEqual(seqs, [seqs[0], seqs[0] + 1, seqs[0] + 2])

    def test_validation_errors_are_flat(self):
        res = self.client.post('/api/enquiries', {'type': 'contact', 'name': 'A', 'email': 'nope', 'message': 'short'}, format='json')
        self.assertEqual(res.status_code, 422)
        details = res.json()['error']['details']
        self.assertEqual(set(details), {'name', 'email', 'message'})

    def test_writes_require_trusted_origin(self):
        client = APIClient(HTTP_ORIGIN='https://evil.example')
        res = client.post('/api/enquiries', {'type': 'contact'}, format='json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(APIClient().post('/api/enquiries', {}, format='json').status_code, 403)


class AuthTests(ApiTestCase):
    def test_login_me_logout(self):
        res = self.login()
        self.assertIn('hb_admin_token', res.cookies)
        me = self.client.get('/api/auth/me').json()['data']
        self.assertEqual(me['roleName'], 'Administrator')
        self.assertIn('tours.publish', me['permissions'])
        self.client.post('/api/auth/logout')
        self.assertEqual(self.client.get('/api/auth/me').status_code, 401)

    def test_bad_credentials(self):
        res = self.client.post('/api/auth/login', {'email': 'admin@test.example', 'password': 'wrong-password-123'}, format='json')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()['error']['message'], 'Those credentials do not match our records.')

    def test_demo_staff_cannot_sign_in(self):
        res = self.client.post('/api/auth/login', {'email': 'amani.consultant@example.com', 'password': 'anything-at-all'}, format='json')
        self.assertEqual(res.status_code, 401)

    def test_admin_routes_need_session(self):
        self.assertEqual(self.client.get('/api/admin/tours').status_code, 401)

    def test_garbage_cookie_is_cleared(self):
        self.client.cookies['hb_admin_token'] = 'not-a-jwt'
        res = self.client.get('/api/auth/me')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.cookies['hb_admin_token'].value, '')


class ContentAdminTests(ApiTestCase):
    def tour_payload(self, **overrides):
        payload = {
            'title': 'Test Weekend Package', 'category': 'locals', 'summary': 'A short test weekend away.',
            'description': 'A longer description of the test weekend package.', 'priceFrom': 12000,
            'currency': 'KES', 'durationDays': 3, 'countries': ['Kenya'],
            'heroImage': {'url': '/images/diani-beach-palms.jpg', 'alt': 'Diani'},
            'gallery': [{'url': '/images/kenya-coast-sunset.jpg', 'alt': 'Sunset'}],
        }
        payload.update(overrides)
        return payload

    def test_tour_crud(self):
        self.login()
        res = self.client.post('/api/admin/tours', self.tour_payload(), format='json')
        self.assertEqual(res.status_code, 201, res.content)
        tour = res.json()['data']
        self.assertEqual(tour['durationNights'], 2)
        self.assertEqual(tour['status'], 'draft')
        self.assertEqual(len(tour['gallery']), 1)

        res = self.client.patch(f"/api/admin/tours/{tour['id']}", {'title': 'Renamed', 'priceFrom': 13000}, format='json')
        self.assertEqual(res.json()['data']['slug'], 'test-weekend-package')  # slug kept on rename

        res = self.client.patch(f"/api/admin/tours/{tour['id']}/status", {'status': 'published'}, format='json')
        self.assertEqual(res.json()['data']['status'], 'published')
        self.assertEqual(self.client.get('/api/tours/test-weekend-package').status_code, 200)

        res = self.client.delete(f"/api/admin/tours/{tour['id']}")
        self.assertEqual(res.status_code, 200)

    def test_tour_must_use_leaf_category(self):
        self.login()
        res = self.client.post('/api/admin/tours', self.tour_payload(category='safaris'), format='json')
        self.assertEqual(res.status_code, 422)
        self.assertIn('category', res.json()['error']['details'])

    def test_duplicate_title_gets_suffixed_slug(self):
        self.login()
        a = self.client.post('/api/admin/tours', self.tour_payload(), format='json').json()['data']
        b = self.client.post('/api/admin/tours', self.tour_payload(), format='json').json()['data']
        self.assertEqual(b['slug'], f"{a['slug']}-2")

    def test_author_cannot_publish_or_delete(self):
        self.make_user('Author', 'author@test.example')
        self.login('author@test.example')
        created = self.client.post('/api/admin/tours', self.tour_payload(), format='json')
        self.assertEqual(created.status_code, 201)
        tour_id = created.json()['data']['id']
        self.assertEqual(self.client.patch(f'/api/admin/tours/{tour_id}/status', {'status': 'published'}, format='json').status_code, 403)
        self.assertEqual(self.client.patch(f'/api/admin/tours/{tour_id}', {'status': 'published'}, format='json').status_code, 403)
        self.assertEqual(self.client.delete(f'/api/admin/tours/{tour_id}').status_code, 403)
        self.assertEqual(self.client.post('/api/admin/tours', self.tour_payload(status='published'), format='json').status_code, 403)

    def test_bulk_status(self):
        self.login()
        ids = [str(t.id) for t in Tour.objects.filter(currency='KES')[:3]]
        res = self.client.patch('/api/admin/tours/bulk/status', {'ids': ids, 'status': 'draft'}, format='json')
        self.assertEqual(res.json()['data']['count'], 3)
        self.assertEqual(Tour.objects.filter(pk__in=ids, status='draft').count(), 3)

    def test_destination_places_replace(self):
        self.login()
        dest = self.client.get('/api/destinations/france').json()['data']
        res = self.client.patch(f"/api/admin/destinations/{dest['id']}", {
            'parks': [{'name': 'Paris'}, {'name': 'Nice', 'blurb': 'Riviera'}],
        }, format='json')
        self.assertEqual([p['name'] for p in res.json()['data']['parks']], ['Paris', 'Nice'])

    def test_settings_merge(self):
        self.login()
        res = self.client.patch('/api/admin/settings', {'contact': {'phone': '+254 711 111 111'}}, format='json')
        contact = res.json()['data']['contact']
        self.assertEqual(contact['phone'], '+254 711 111 111')
        self.assertEqual(contact['email'], 'hello@holidaybankexpeditions.com')

    def test_settings_rejects_youtube_url(self):
        self.login()
        res = self.client.patch('/api/admin/settings', {'video': {'youtubeId': 'https://youtu.be/abc'}}, format='json')
        self.assertEqual(res.status_code, 422)

    def test_blog_tags_filter(self):
        body = self.client.get('/api/blog?tag=europe').json()
        self.assertTrue(body['data'] and all('europe' in p['tags'] for p in body['data']))

    def nav(self, **overrides):
        item = {'id': 'a', 'label': 'Safaris', 'href': '/tours?category=safaris', 'visible': True, 'children': [
            {'id': 'b', 'label': 'Kenyan Safaris', 'href': '/tours?category=kenyan-safaris',
             'image': {'url': '/images/mara-cheetah.jpg', 'alt': ''}},
            {'id': 'c', 'label': 'Hidden', 'href': '/about', 'visible': False},
        ]}
        item.update(overrides)
        return [item, {'id': 'd', 'label': 'Contact', 'href': '/contact'}]

    def test_navigation_starts_automatic(self):
        self.assertEqual(self.client.get('/api/settings').json()['data']['navigation'], [])

    def test_navigation_save_and_reset(self):
        self.login()
        res = self.client.patch('/api/admin/settings', {'navigation': self.nav()}, format='json')
        self.assertEqual(res.status_code, 200, res.content)
        nav = self.client.get('/api/settings').json()['data']['navigation']
        self.assertEqual([i['label'] for i in nav], ['Safaris', 'Contact'])
        self.assertEqual(nav[0]['children'][0]['image']['url'], '/images/mara-cheetah.jpg')
        self.assertFalse(nav[0]['children'][1]['visible'])
        self.assertTrue(nav[1]['visible'])  # defaults to shown
        # Other sections are untouched by a navigation save.
        self.assertEqual(self.client.get('/api/settings').json()['data']['contact']['email'], 'hello@holidaybankexpeditions.com')

        res = self.client.patch('/api/admin/settings', {'navigation': []}, format='json')
        self.assertEqual(res.json()['data']['navigation'], [])

    def test_navigation_rejects_unsafe_links_and_blank_titles(self):
        self.login()
        for bad in ({'href': 'javascript:alert(1)'}, {'href': '//evil.example'}, {'label': ''}):
            res = self.client.patch('/api/admin/settings', {'navigation': self.nav(**bad)}, format='json')
            self.assertEqual(res.status_code, 422, bad)

    def test_navigation_linked_items(self):
        self.login()
        linked = [
            {'id': 'k', 'label': '', 'source': {'type': 'area', 'slug': 'kenyan'}},
            {'id': 's', 'label': 'Our safaris', 'source': {'type': 'category', 'slug': 'safaris'}, 'showChildren': False},
            {'id': 'f', 'source': {'type': 'destination', 'slug': 'france'}},
        ]
        res = self.client.patch('/api/admin/settings', {'navigation': linked}, format='json')
        self.assertEqual(res.status_code, 200, res.content)
        nav = res.json()['data']['navigation']
        self.assertEqual(nav[0]['source'], {'type': 'area', 'slug': 'kenyan'})
        self.assertEqual(nav[0]['label'], '')  # inherits the area's name when rendered
        self.assertFalse(nav[1]['showChildren'])

        res = self.client.patch('/api/admin/settings', {'navigation': [
            {'id': 'x', 'source': {'type': 'category', 'slug': 'atlantis'}},
        ]}, format='json')
        self.assertEqual(res.status_code, 422)
        self.assertIn('navigation.0.source.slug', res.json()['error']['details'])

    def test_navigation_needs_settings_permission(self):
        self.make_user('Author', 'author@test.example')
        self.login('author@test.example')
        res = self.client.patch('/api/admin/settings', {'navigation': self.nav()}, format='json')
        self.assertEqual(res.status_code, 403)


class TravelAreaTests(ApiTestCase):
    def test_area_tree(self):
        groups = self.client.get('/api/areas').json()['data']
        self.assertEqual([g['name'] for g in groups], ['Kenyan', 'Europe', 'Africa', 'Asia & Middle East'])
        kenyan = groups[0]
        self.assertEqual([a['name'] for a in kenyan['children']],
                         ['Diani', 'Watamu/Malindi', 'Maasai Mara', 'Amboseli', 'Tsavo'])
        by_slug = {a['slug']: a for g in groups for a in g['children']}
        self.assertEqual(by_slug['maasai-mara']['tourCount'], 5)
        self.assertEqual(by_slug['watamu-malindi']['tourCount'], 0)
        # Distinct tours: the group is not the sum of its areas when a tour is in two.
        europe = groups[1]
        self.assertEqual(europe['tourCount'], 6)
        self.assertEqual(sum(a['tourCount'] for a in europe['children']), 7)

    def test_kenyan_area_cards(self):
        kenyan = self.client.get('/api/areas').json()['data'][0]
        for area in kenyan['children']:
            self.assertEqual(area['tag'], 'Locals / Kenya')
            self.assertTrue(area['description'])
            self.assertTrue(area['image']['url'].startswith('/images/'))
            self.assertEqual(area['placeCount'], 1, area['slug'])
        watamu = next(a for a in kenyan['children'] if a['slug'] == 'watamu-malindi')
        self.assertEqual(watamu['tourCount'], 0)

    def test_filter_by_area_and_group(self):
        mara = self.client.get('/api/tours?area=maasai-mara&limit=50').json()
        self.assertEqual(mara['meta']['total'], 5)
        self.assertTrue(all(any(a['slug'] == 'maasai-mara' for a in t['areas']) for t in mara['data']))
        kenyan = self.client.get('/api/tours?area=kenyan&limit=50').json()
        self.assertEqual(kenyan['meta']['total'], 8)
        self.assertEqual(self.client.get('/api/tours?area=atlantis').json()['meta']['total'], 0)
        self.assertEqual(mara['data'][0]['areas'][0]['group']['slug'], 'kenyan')

    def test_tour_areas_edit(self):
        self.login()
        tour = Tour.objects.get(title='Lake Naivasha Weekend')
        res = self.client.patch(f'/api/admin/tours/{tour.id}', {'areas': ['diani', 'tsavo']}, format='json')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(sorted(a['slug'] for a in res.json()['data']['areas']), ['diani', 'tsavo'])
        res = self.client.patch(f'/api/admin/tours/{tour.id}', {'areas': ['atlantis']}, format='json')
        self.assertEqual(res.status_code, 422)
        self.assertIn('areas', res.json()['error']['details'])


class EnquiryPipelineTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.enquiry = Enquiry.objects.filter(status='new', assignee__isnull=True).first()

    def test_list_meta_counts(self):
        self.login()
        meta = self.client.get('/api/admin/enquiries?limit=5').json()['meta']
        self.assertIn('statusCounts', meta)
        self.assertGreaterEqual(meta['unassignedCount'], 1)
        self.assertGreaterEqual(meta['overdueCount'], 1)

    def test_claim_status_contact_note(self):
        self.login()
        url = f'/api/admin/enquiries/{self.enquiry.id}'
        claimed = self.client.patch(f'{url}/assignee', {}, format='json').json()['data']
        self.assertEqual(claimed['status'], 'assigned')
        self.assertEqual(claimed['assignee']['email'], 'admin@test.example')

        contacted = self.client.post(f'{url}/contacted', {'followUpAt': '2030-01-01T09:00:00Z'}, format='json').json()['data']
        self.assertEqual(contacted['status'], 'in_progress')

        won = self.client.patch(f'{url}/status', {'status': 'won'}, format='json').json()['data']
        self.assertIsNotNone(won['closedAt'])
        self.assertIsNone(won['followUpAt'])

        detail = self.client.post(f'{url}/notes', {'note': 'Deposit received.'}, format='json').json()['data']
        types = [e['type'] for e in detail['events']]
        self.assertEqual(types[0], 'note')
        self.assertIn('assigned', types)
        self.assertIn('contacted', types)

    def test_consultant_cannot_take_others_work(self):
        consultant = self.make_user('Travel Consultant', 'tc@test.example')
        consultant.role.permissions = ['enquiries.view', 'enquiries.edit']
        consultant.role.save()
        owned = Enquiry.objects.filter(assignee__isnull=False).exclude(assignee=consultant).first()
        self.login('tc@test.example')
        res = self.client.patch(f'/api/admin/enquiries/{owned.id}/assignee', {}, format='json')
        self.assertEqual(res.status_code, 409)

    def test_bulk_assign_includes_unassigned(self):
        self.login()
        ids = [str(e.id) for e in Enquiry.objects.filter(assignee__isnull=True)]
        res = self.client.patch('/api/admin/enquiries/bulk/assign', {'ids': ids, 'assigneeId': str(self.admin.id)}, format='json')
        self.assertEqual(res.json()['data']['count'], len(ids))


class AccessControlTests(ApiTestCase):
    def test_cannot_delete_self_or_last_manager(self):
        self.login()
        self.assertEqual(self.client.delete(f'/api/admin/users/{self.admin.id}').status_code, 400)
        editor_role = Role.objects.get(name='Editor')
        res = self.client.patch(f'/api/admin/users/{self.admin.id}', {'roleId': str(editor_role.id)}, format='json')
        self.assertEqual(res.status_code, 400)

    def test_locked_role_is_immutable(self):
        self.login()
        admin_role = Role.objects.get(locked=True)
        self.assertEqual(self.client.patch(f'/api/admin/roles/{admin_role.id}', {'name': 'Renamed role'}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(f'/api/admin/roles/{admin_role.id}').status_code, 400)

    def test_create_user_is_audited_and_password_checked(self):
        self.login()
        role = Role.objects.get(name='Editor')
        weak = self.client.post('/api/admin/users', {'email': 'n@test.example', 'name': 'New', 'password': 'short', 'roleId': str(role.id)}, format='json')
        self.assertEqual(weak.status_code, 422)
        ok = self.client.post('/api/admin/users', {'email': 'n@test.example', 'name': 'New', 'password': 'a-very-long-passphrase', 'roleId': str(role.id)}, format='json')
        self.assertEqual(ok.status_code, 201, ok.content)
        self.assertTrue(AuditLog.objects.filter(action='user.create', target_label='n@test.example').exists())

    def test_unknown_permission_rejected(self):
        self.login()
        res = self.client.post('/api/admin/roles', {'name': 'Odd', 'permissions': ['tours.fly']}, format='json')
        self.assertEqual(res.status_code, 422)


class UploadTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.media_root = tempfile.mkdtemp()
        from pathlib import Path

        self.override = override_settings(MEDIA_ROOT=Path(self.media_root))
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def image_file(self, fmt='PNG', name='photo.png'):
        buffer = io.BytesIO()
        Image.new('RGB', (40, 30), 'orange').save(buffer, format=fmt)
        buffer.seek(0)
        buffer.name = name
        return buffer

    def test_upload_registers_asset_and_can_be_removed(self):
        self.login()
        res = self.client.post('/api/admin/uploads', {'file': self.image_file()}, format='multipart')
        self.assertEqual(res.status_code, 201, res.content)
        data = res.json()['data']
        self.assertTrue(data['url'].endswith('.png'))
        asset = self.client.get('/api/admin/media?q=photo').json()['data'][0]
        self.assertEqual(asset['width'], 40)
        removed = self.client.delete(f"/api/admin/uploads/{data['filename']}").json()['data']
        self.assertTrue(removed['deleted'])

    def test_rejects_non_images_and_traversal(self):
        self.login()
        fake = io.BytesIO(b'not an image at all')
        fake.name = 'x.png'
        self.assertEqual(self.client.post('/api/admin/uploads', {'file': fake}, format='multipart').status_code, 400)
        self.assertIn(self.client.delete('/api/admin/uploads/..%2Fsettings.py').status_code, (400, 404))
