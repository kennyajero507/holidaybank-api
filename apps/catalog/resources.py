"""Wire shapes, input schemas and write logic for countries, categories, destinations and tours."""
from django.db.models import Count, Prefetch, Q
from rest_framework import serializers

from apps.common.crud import Resource, assign
from apps.common.exceptions import ApiError
from apps.common.slugs import slugify
from apps.common.validation import (
    STATUS_CHOICES,
    BooleanString,
    ImageSchema,
    PaginationQuery,
    SearchField,
    SeoSchema,
    StringList,
)
from apps.media.services import image_shape, resolve_image

from .models import (
    CategoryKind,
    Country,
    Destination,
    Difficulty,
    Place,
    Region,
    Tour,
    TourCategory,
    TourImage,
    TravelArea,
)

# ---------------------------------------------------------------------------
# Countries
# ---------------------------------------------------------------------------


def country_shape(c: Country) -> dict:
    return {
        'id': str(c.id),
        '_id': str(c.id),
        'name': c.name,
        'slug': c.slug,
        'isoCode': c.iso_code,
        'region': c.region,
        'regionLabel': Region(c.region).label,
    }


def resolve_countries(values: list[str]) -> list[Country]:
    """Accepts names or slugs, case-insensitively."""
    found, unknown = [], []
    for value in values:
        match = Country.objects.filter(Q(name__iexact=value) | Q(slug__iexact=value)).first()
        (found if match else unknown).append(match or value)
    if unknown:
        raise ApiError.unprocessable(details={'countries': f'Unknown country: {", ".join(unknown)}.'})
    return found


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------


def category_ref(c: TourCategory | None) -> dict | None:
    if c is None:
        return None
    return {'slug': c.slug, 'name': c.name, 'kind': c.kind}


def category_shape(c: TourCategory, children: list | None = None) -> dict:
    shape = {
        'id': str(c.id),
        '_id': str(c.id),
        'name': c.name,
        'slug': c.slug,
        'kind': c.kind,
        'eyebrow': c.eyebrow,
        'navLabel': c.nav_label or c.name,
        'description': c.description,
        'heroImage': image_shape(c.hero_image),
        'parent': category_ref(c.parent),
        'order': c.order,
        'status': c.status,
        'isSample': c.is_sample,
        'sourceNote': c.source_note or None,
    }
    if children is not None:
        shape['children'] = children
    return shape


# ---------------------------------------------------------------------------
# Travel areas (regional groupings)
# ---------------------------------------------------------------------------


def area_ref(a: TravelArea) -> dict:
    group = a.parent if a.parent_id else None
    return {'slug': a.slug, 'name': a.name, 'group': {'slug': group.slug, 'name': group.name} if group else None}


def area_shape(a: TravelArea, children: list | None = None) -> dict:
    shape = {
        'id': str(a.id),
        '_id': str(a.id),
        'name': a.name,
        'slug': a.slug,
        'description': a.description,
        'tag': a.tag,
        'image': image_shape(a.image),
        # Annotated by the tree view; counted directly elsewhere.
        'placeCount': a.place_count if hasattr(a, 'place_count') else a.places.count(),
        'parent': {'slug': a.parent.slug, 'name': a.parent.name} if a.parent_id else None,
        'order': a.order,
        'status': a.status,
        'isSample': a.is_sample,
    }
    if children is not None:
        shape['children'] = children
    return shape


def resolve_areas(slugs: list[str]) -> list[TravelArea]:
    found = list(TravelArea.objects.filter(slug__in=slugs))
    unknown = sorted(set(slugs) - {a.slug for a in found})
    if unknown:
        raise ApiError.unprocessable(details={'areas': f'Unknown area: {", ".join(unknown)}.'})
    return found


class CategorySchema(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=80)
    slug = serializers.CharField(max_length=80, required=False, allow_blank=True)
    parent = serializers.CharField(max_length=80, required=False, allow_null=True, allow_blank=True)
    kind = serializers.ChoiceField(choices=CategoryKind.values)
    eyebrow = serializers.CharField(max_length=80, required=False, allow_blank=True)
    navLabel = serializers.CharField(max_length=80, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    heroImage = ImageSchema(required=False, allow_null=True)
    order = serializers.IntegerField(min_value=0, default=0)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class CategoryQuery(PaginationQuery):
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    kind = serializers.ChoiceField(choices=CategoryKind.values, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['order-asc', 'name-asc', 'newest'], required=False)


def apply_category(obj: TourCategory, data: dict, creating: bool) -> None:
    assign(obj, data, {'name': 'name', 'kind': 'kind', 'eyebrow': 'eyebrow', 'navLabel': 'nav_label',
                       'description': 'description', 'order': 'order', 'status': 'status', 'isSample': 'is_sample', 'sourceNote': 'source_note'})
    if 'parent' in data:
        parent = None
        if data['parent']:
            parent = TourCategory.objects.filter(slug=data['parent']).first()
            if parent is None:
                raise ApiError.unprocessable(details={'parent': 'That parent category does not exist.'})
            if obj.pk and parent.pk == obj.pk:
                raise ApiError.unprocessable(details={'parent': 'A category cannot be its own parent.'})
        obj.parent = parent
    if 'heroImage' in data:
        obj.hero_image = resolve_image(data['heroImage'])
    obj.save()


categories = Resource(
    model=TourCategory,
    label='category',
    perm='categories',
    path='categories',
    shape=lambda c: category_shape(c),
    create_schema=CategorySchema,
    update_schema=CategorySchema,
    list_query=CategoryQuery,
    apply=apply_category,
    title_field='name',
    search_fields=['name', 'description'],
    sorts={'order-asc': ['order', 'name'], 'name-asc': ['name'], 'newest': ['-created_at']},
    default_sort=['order', 'name'],
    filter=lambda qs, q: qs.filter(kind=q['kind']) if q.get('kind') else qs,
    queryset=lambda: TourCategory.objects.select_related('parent', 'hero_image'),
    tags=lambda c: ['categories', 'tours', 'home'],
    public_list=False,  # the public tree is served by CategoryTreeView
)


# ---------------------------------------------------------------------------
# Destinations
# ---------------------------------------------------------------------------


def place_shape(p: Place) -> dict:
    return {
        'name': p.name,
        'slug': p.slug,
        'kind': p.kind or None,
        'blurb': p.blurb or None,
        'image': image_shape(p.image),
        'bestTime': p.best_time or None,
        'highlights': p.highlights or [],
    }


def destination_shape(d: Destination) -> dict:
    places = list(d.places.all())
    return {
        'id': str(d.id),
        '_id': str(d.id),
        'name': d.name,
        'slug': d.slug,
        'country': d.country.name,
        'countrySlug': d.country.slug,
        'region': d.country.region,
        'regionLabel': Region(d.country.region).label,
        'tagline': d.tagline or None,
        'categoryLabel': d.category_label,
        'overview': d.overview,
        'heroImage': image_shape(d.hero_image),
        'cardImage': image_shape(d.card_image),
        'highlights': d.highlights or [],
        'bestTime': d.best_time,
        # `parks` is the wire name the web app has always used for a
        # destination's places; they are cities and beaches as well as parks.
        'parks': [place_shape(p) for p in places],
        'parkCount': len(places),
        'tourCount': getattr(d, 'tour_count', None),
        'featured': d.featured,
        'status': d.status,
        'order': d.order,
        'seo': d.seo,
        'isSample': d.is_sample,
        'sourceNote': d.source_note or None,
        'createdAt': d.created_at,
        'updatedAt': d.updated_at,
    }


class PlaceSchema(serializers.Serializer):
    name = serializers.CharField(max_length=120, error_messages={'blank': 'Each place needs a name.'})
    slug = serializers.CharField(max_length=120, required=False, allow_blank=True)
    kind = serializers.CharField(max_length=40, required=False, allow_blank=True, allow_null=True)
    blurb = serializers.CharField(max_length=300, required=False, allow_blank=True, allow_null=True)
    image = ImageSchema(required=False, allow_null=True)
    bestTime = serializers.CharField(max_length=120, required=False, allow_blank=True, allow_null=True)
    highlights = StringList(default=list)


class BestTimeSchema(serializers.Serializer):
    months = StringList(max_items=12, default=list)
    note = serializers.CharField(max_length=400, required=False, allow_blank=True)


class DestinationSchema(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120, error_messages={'min_length': 'Give the destination a name.'})
    slug = serializers.CharField(max_length=120, required=False, allow_blank=True)
    country = serializers.CharField(max_length=80)
    tagline = serializers.CharField(max_length=180, required=False, allow_blank=True, allow_null=True)
    categoryLabel = serializers.CharField(max_length=60, default='Destination')
    overview = serializers.CharField(min_length=20, error_messages={'min_length': 'Write an overview.'})
    heroImage = ImageSchema()
    cardImage = ImageSchema()
    highlights = StringList(default=list)
    bestTime = BestTimeSchema(required=False, allow_null=True)
    parks = serializers.ListField(child=PlaceSchema(), required=False, max_length=40)
    featured = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    order = serializers.IntegerField(min_value=0, default=0)
    seo = SeoSchema(required=False, allow_null=True)
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class DestinationQuery(PaginationQuery):
    country = serializers.CharField(max_length=80, required=False)
    region = serializers.ChoiceField(choices=Region.values, required=False)
    featured = BooleanString()
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['order-asc', 'newest', 'name-asc', 'name-desc'], required=False)


def filter_destinations(qs, q):
    if q.get('country'):
        qs = qs.filter(Q(country__name__iexact=q['country']) | Q(country__slug__iexact=q['country']))
    if q.get('region'):
        qs = qs.filter(country__region=q['region'])
    if 'featured' in q:
        qs = qs.filter(featured=q['featured'])
    return qs


def apply_destination(obj: Destination, data: dict, creating: bool) -> None:
    assign(obj, data, {'name': 'name', 'tagline': 'tagline', 'categoryLabel': 'category_label',
                       'overview': 'overview', 'highlights': 'highlights', 'bestTime': 'best_time',
                       'featured': 'featured', 'status': 'status', 'order': 'order', 'seo': 'seo',
                       'isSample': 'is_sample', 'sourceNote': 'source_note'})
    if obj.tagline is None:
        obj.tagline = ''
    if 'country' in data:
        country = resolve_countries([data['country']])[0]
        clash = Destination.objects.filter(country=country).exclude(pk=obj.pk).first()
        if clash:
            raise ApiError.unprocessable(details={'country': f'{country.name} already has a destination page ({clash.name}).'})
        obj.country = country
    if 'heroImage' in data:
        obj.hero_image = resolve_image(data['heroImage'])
    if 'cardImage' in data:
        obj.card_image = resolve_image(data['cardImage'])
    obj.save()

    if 'parks' in data:
        # The dashboard edits places as one list and PUTs it back whole.
        obj.places.all().delete()
        used = set()
        for index, place in enumerate(data['parks']):
            slug = slugify(place.get('slug') or place['name']) or f'place-{index + 1}'
            while slug in used:
                slug = f'{slug}-{index + 1}'
            used.add(slug)
            Place.objects.create(
                destination=obj,
                name=place['name'],
                slug=slug,
                kind=place.get('kind') or '',
                blurb=place.get('blurb') or '',
                image=resolve_image(place.get('image')),
                best_time=place.get('bestTime') or '',
                highlights=place.get('highlights') or [],
                order=index,
            )


destinations = Resource(
    model=Destination,
    label='destination',
    perm='destinations',
    path='destinations',
    shape=destination_shape,
    create_schema=DestinationSchema,
    update_schema=DestinationSchema,
    list_query=DestinationQuery,
    apply=apply_destination,
    title_field='name',
    search_fields=['name', 'tagline', 'country__name', 'places__name'],
    sorts={'order-asc': ['order', 'name'], 'newest': ['-created_at'], 'name-asc': ['name'], 'name-desc': ['-name']},
    default_sort=['order', 'name'],
    filter=filter_destinations,
    queryset=lambda: Destination.objects.select_related('country', 'hero_image', 'card_image')
    .prefetch_related(Prefetch('places', queryset=Place.objects.select_related('image')))
    .annotate(tour_count=Count('tours', filter=Q(tours__status='published'), distinct=True)),
    tags=lambda d: ['destinations', f'destination:{d.slug}', 'home'],
)


# ---------------------------------------------------------------------------
# Tours
# ---------------------------------------------------------------------------


def duration_label(days: int, nights: int | None) -> str:
    n = nights if nights is not None else max(0, days - 1)
    if days == 1 and n == 0:
        return 'Day trip'
    return f'{days} {"Day" if days == 1 else "Days"} / {n} {"Night" if n == 1 else "Nights"}'


def tour_shape(t: Tour) -> dict:
    category = t.category
    group = category.parent if category.parent_id else None
    destination = t.destination
    return {
        'id': str(t.id),
        '_id': str(t.id),
        'title': t.title,
        'slug': t.slug,
        'category': category.slug,
        'categoryInfo': {
            'slug': category.slug,
            'name': category.name,
            'kind': category.kind,
            'group': category_ref(group),
        },
        'summary': t.summary,
        'description': t.description,
        'priceFrom': t.price_from,
        'currency': t.currency,
        'priceBasis': t.price_basis,
        'durationDays': t.duration_days,
        'durationNights': t.duration_nights,
        'durationLabel': duration_label(t.duration_days, t.duration_nights),
        'groupSizeMax': t.group_size_max,
        'difficulty': t.difficulty,
        'rating': t.rating,
        'reviewCount': t.review_count,
        'destination': (
            {
                'id': str(destination.id),
                '_id': str(destination.id),
                'name': destination.name,
                'slug': destination.slug,
                'country': destination.country.name,
                'heroImage': image_shape(destination.hero_image),
            }
            if destination
            else None
        ),
        'countries': [c.name for c in t.countries.all()],
        'areas': [area_ref(a) for a in t.areas.all()],
        'locationLabel': t.location_label or None,
        'highlights': t.highlights or [],
        'itinerary': t.itinerary or [],
        'inclusions': t.inclusions or [],
        'exclusions': t.exclusions or [],
        'heroImage': image_shape(t.hero_image),
        'gallery': [image_shape(link.image) for link in t.tourimage_set.all()],
        'featured': t.featured,
        'bestSelling': t.best_selling,
        'status': t.status,
        'order': t.order,
        'seo': t.seo,
        'parks': t.parks or [],
        'gameDriveCount': t.game_drive_count,
        'conservancyFeesIncluded': t.conservancy_fees_included,
        'departsFrom': t.departs_from or None,
        'departureDates': t.departure_dates or [],
        'visaSupport': t.visa_support,
        'flightsIncluded': t.flights_included,
        'isSample': t.is_sample,
        'sourceNote': t.source_note or None,
        'createdAt': t.created_at,
        'updatedAt': t.updated_at,
    }


class ItineraryDaySchema(serializers.Serializer):
    day = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=160, error_messages={'blank': 'Each day needs a title.'})
    description = serializers.CharField(required=False, allow_blank=True)
    activities = StringList(default=list)
    meals = serializers.ListField(
        child=serializers.ChoiceField(choices=['Breakfast', 'Lunch', 'Dinner']), required=False, default=list
    )
    accommodation = serializers.CharField(max_length=160, required=False, allow_blank=True)


class TourSchema(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=140, error_messages={'min_length': 'Give the tour a title.'})
    slug = serializers.CharField(max_length=140, required=False, allow_blank=True)
    category = serializers.CharField(max_length=80)
    summary = serializers.CharField(min_length=10, max_length=300, error_messages={'min_length': 'Write a short summary.'})
    description = serializers.CharField(min_length=20, error_messages={'min_length': 'Write a fuller description.'})
    priceFrom = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    currency = serializers.ChoiceField(choices=['KES', 'USD', 'EUR', 'GBP'], default='KES')
    priceBasis = serializers.CharField(max_length=40, default='per person')
    durationDays = serializers.IntegerField(min_value=1, max_value=60)
    durationNights = serializers.IntegerField(min_value=0, max_value=60, required=False, allow_null=True)
    groupSizeMax = serializers.IntegerField(min_value=1, default=12)
    difficulty = serializers.ChoiceField(choices=Difficulty.values, default='easy')
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, min_value=0, max_value=5, required=False)
    reviewCount = serializers.IntegerField(min_value=0, required=False)
    destination = serializers.UUIDField(required=False, allow_null=True)
    countries = StringList(max_items=10, default=list)
    areas = StringList(max_items=20, item_max=80)
    locationLabel = serializers.CharField(max_length=80, required=False, allow_blank=True, allow_null=True)
    highlights = StringList(default=list)
    itinerary = serializers.ListField(child=ItineraryDaySchema(), required=False, default=list, max_length=60)
    inclusions = StringList(default=list)
    exclusions = StringList(default=list)
    heroImage = ImageSchema()
    gallery = serializers.ListField(child=ImageSchema(), required=False, default=list, max_length=40)
    featured = serializers.BooleanField(default=False)
    bestSelling = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    order = serializers.IntegerField(min_value=0, default=0)
    seo = SeoSchema(required=False, allow_null=True)
    parks = StringList(max_items=20, required=False)
    gameDriveCount = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    conservancyFeesIncluded = serializers.BooleanField(required=False, allow_null=True)
    departsFrom = serializers.CharField(max_length=120, required=False, allow_blank=True, allow_null=True)
    departureDates = serializers.ListField(child=serializers.DateField(), required=False, max_length=60)
    visaSupport = serializers.BooleanField(required=False, allow_null=True)
    flightsIncluded = serializers.BooleanField(required=False, allow_null=True)
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


TOUR_SORTS = {
    'recommended': ['-featured', 'order', '-created_at'],
    # Prices are in KES and USD; sorting groups by currency first rather than
    # pretending KSh 8,200 is more than $4,200.
    'price-asc': ['currency', 'price_from'],
    'price-desc': ['currency', '-price_from'],
    'duration-asc': ['duration_days', 'order'],
    'newest': ['-created_at'],
    'title-asc': ['title'],
    'title-desc': ['-title'],
}


class TourQuery(PaginationQuery):
    category = serializers.CharField(max_length=80, required=False)
    country = serializers.CharField(max_length=80, required=False)
    # A travel area slug; a group ("kenyan") includes every area beneath it.
    area = serializers.CharField(max_length=80, required=False)
    region = serializers.ChoiceField(choices=Region.values, required=False)
    destination = serializers.CharField(max_length=120, required=False)
    featured = BooleanString()
    bestSelling = BooleanString()
    q = SearchField()
    minPrice = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False)
    maxPrice = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False)
    currency = serializers.ChoiceField(choices=['KES', 'USD', 'EUR', 'GBP'], required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    sort = serializers.ChoiceField(choices=list(TOUR_SORTS), required=False)


def filter_tours(qs, q):
    if q.get('category'):
        category = TourCategory.objects.filter(slug=q['category']).first()
        # An unknown category matches nothing rather than everything.
        qs = qs.filter(category_id__in=category.descendant_ids()) if category else qs.none()
    if q.get('country'):
        qs = qs.filter(Q(countries__name__iexact=q['country']) | Q(countries__slug__iexact=q['country']))
    if q.get('area'):
        area = TravelArea.objects.filter(slug=q['area'], status='published').first()
        qs = qs.filter(areas__in=area.descendant_ids()) if area else qs.none()
    if q.get('region'):
        qs = qs.filter(countries__region=q['region'])
    if q.get('destination'):
        value = q['destination']
        qs = qs.filter(destination_id=value) if _looks_like_uuid(value) else qs.filter(destination__slug=value)
    if 'featured' in q:
        qs = qs.filter(featured=q['featured'])
    if 'bestSelling' in q:
        qs = qs.filter(best_selling=q['bestSelling'])
    if q.get('currency'):
        qs = qs.filter(currency=q['currency'])
    if q.get('minPrice') is not None:
        qs = qs.filter(price_from__gte=q['minPrice'])
    if q.get('maxPrice') is not None:
        qs = qs.filter(price_from__lte=q['maxPrice'])
    return qs.distinct()


def _looks_like_uuid(value: str) -> bool:
    import uuid

    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def apply_tour(obj: Tour, data: dict, creating: bool) -> None:
    assign(obj, data, {
        'title': 'title', 'summary': 'summary', 'description': 'description', 'priceFrom': 'price_from',
        'currency': 'currency', 'priceBasis': 'price_basis', 'durationDays': 'duration_days',
        'groupSizeMax': 'group_size_max', 'difficulty': 'difficulty', 'rating': 'rating',
        'reviewCount': 'review_count', 'highlights': 'highlights', 'inclusions': 'inclusions',
        'exclusions': 'exclusions', 'featured': 'featured', 'bestSelling': 'best_selling', 'status': 'status',
        'order': 'order', 'seo': 'seo', 'parks': 'parks', 'gameDriveCount': 'game_drive_count',
        'conservancyFeesIncluded': 'conservancy_fees_included', 'visaSupport': 'visa_support',
        'flightsIncluded': 'flights_included', 'isSample': 'is_sample', 'sourceNote': 'source_note',
    })
    if 'locationLabel' in data:
        obj.location_label = data['locationLabel'] or ''
    if 'departsFrom' in data:
        obj.departs_from = data['departsFrom'] or ''
    if 'departureDates' in data:
        obj.departure_dates = [d.isoformat() for d in data['departureDates']]
    if 'itinerary' in data:
        obj.itinerary = [dict(day) for day in data['itinerary']]

    # Nights default to days - 1 unless given explicitly.
    if data.get('durationNights') is not None:
        obj.duration_nights = data['durationNights']
    elif creating or 'durationDays' in data:
        if creating or obj.duration_nights is None:
            obj.duration_nights = max(0, obj.duration_days - 1)

    if 'category' in data:
        category = TourCategory.objects.filter(slug=data['category']).first()
        if category is None:
            raise ApiError.unprocessable(details={'category': 'That category does not exist.'})
        if category.children.exists():
            raise ApiError.unprocessable(details={'category': f'Choose one of the categories inside "{category.name}".'})
        obj.category = category
    if 'destination' in data:
        obj.destination = Destination.objects.filter(pk=data['destination']).first() if data['destination'] else None
        if data['destination'] and obj.destination is None:
            raise ApiError.unprocessable(details={'destination': 'That destination does not exist.'})
    if 'heroImage' in data:
        obj.hero_image = resolve_image(data['heroImage'])
    obj.save()

    if 'countries' in data:
        obj.countries.set(resolve_countries(data['countries']))
    if 'areas' in data:
        obj.areas.set(resolve_areas(data['areas']))
    if 'gallery' in data:
        TourImage.objects.filter(tour=obj).delete()
        seen = set()
        for index, image in enumerate(data['gallery']):
            asset = resolve_image(image)
            if asset.pk in seen:
                continue
            seen.add(asset.pk)
            TourImage.objects.create(tour=obj, image=asset, order=index)


def tour_queryset():
    return Tour.objects.select_related(
        'category', 'category__parent', 'hero_image', 'destination', 'destination__country', 'destination__hero_image'
    ).prefetch_related(
        'countries',
        Prefetch('areas', queryset=TravelArea.objects.select_related('parent')),
        Prefetch('tourimage_set', queryset=TourImage.objects.select_related('image')),
    )


tours = Resource(
    model=Tour,
    label='tour',
    perm='tours',
    path='tours',
    shape=tour_shape,
    create_schema=TourSchema,
    update_schema=TourSchema,
    list_query=TourQuery,
    apply=apply_tour,
    search_fields=['title', 'summary', 'location_label', 'countries__name'],
    sorts=TOUR_SORTS,
    default_sort=TOUR_SORTS['recommended'],
    filter=filter_tours,
    queryset=tour_queryset,
    tags=lambda t: ['tours', f'tour:{t.slug}', 'home'],
)
