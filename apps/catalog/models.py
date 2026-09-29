from django.db import models

from apps.common.models import BaseModel, PublishableModel
from apps.media.models import ImageAsset


class Region(models.TextChoices):
    EAST_AFRICA = 'east-africa', 'East Africa'
    EUROPE = 'europe', 'Europe'


class Country(BaseModel):
    """A country Holidaybank sells trips to. Drives filters and destination grouping."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    iso_code = models.CharField(max_length=2, blank=True, default='')
    region = models.CharField(max_length=20, choices=Region.choices, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class CategoryKind(models.TextChoices):
    """What sort of product a category holds. Decides which tour fields apply."""

    LOCAL = 'local', 'Kenyan holiday package'
    INTERNATIONAL = 'international', 'International holiday'
    SAFARI = 'safari', 'Safari'


class TourCategory(PublishableModel):
    """
    The product lines from the original site's navigation:

        Kenyan Packages  > Locals
        International    > Europe
        Safaris          > Kenyan Safaris
                         > Kenya · Tanzania · Uganda · Rwanda

    Top-level rows are groups; tours belong to a leaf. Filtering by a group
    includes every leaf beneath it.
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')
    kind = models.CharField(max_length=20, choices=CategoryKind.choices)
    eyebrow = models.CharField(max_length=80, blank=True, default='')
    nav_label = models.CharField(max_length=80, blank=True, default='', help_text='Label in the site menu.')
    description = models.TextField(blank=True, default='')
    hero_image = models.ForeignKey(ImageAsset, null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'tour categories'

    def __str__(self):
        return f'{self.parent.name} › {self.name}' if self.parent_id else self.name

    def descendant_ids(self) -> list:
        ids = [self.id]
        for child in self.children.all():
            ids += child.descendant_ids()
        return ids


class Destination(PublishableModel):
    """A country page: overview, best time to visit, and the places within it."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    country = models.OneToOneField(Country, on_delete=models.PROTECT, related_name='destination')
    tagline = models.CharField(max_length=180, blank=True, default='')
    category_label = models.CharField(max_length=60, default='Destination')
    overview = models.TextField()
    hero_image = models.ForeignKey(ImageAsset, on_delete=models.PROTECT, related_name='+')
    card_image = models.ForeignKey(ImageAsset, on_delete=models.PROTECT, related_name='+')
    highlights = models.JSONField(default=list, blank=True)
    # {"months": ["June", ...], "note": "..."}
    best_time = models.JSONField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    seo = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Place(BaseModel):
    """A park, city, island or region within a destination (Maasai Mara, Paris, Diani...)."""

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    kind = models.CharField(max_length=40, blank=True, default='', help_text='e.g. National reserve, City, Beach')
    blurb = models.CharField(max_length=300, blank=True, default='')
    image = models.ForeignKey(ImageAsset, null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    best_time = models.CharField(max_length=120, blank=True, default='')
    highlights = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        constraints = [models.UniqueConstraint(fields=['destination', 'slug'], name='unique_place_slug_per_destination')]

    def __str__(self):
        return f'{self.name} ({self.destination.name})'


class TravelArea(PublishableModel):
    """
    Regional groupings for browsing, independent of product line:

        Kenyan              > Diani, Watamu/Malindi, Maasai Mara, Amboseli, Tsavo
        Europe              > Germany, Spain, France, Italy
        Africa              > South Africa, Egypt, Zanzibar, Mauritius
        Asia & Middle East  > Thailand, Malaysia, Singapore, Dubai

    Unlike its single category, a tour can sit in several areas (a
    Mara–Serengeti safari is in Maasai Mara). Filtering by a group includes
    every area beneath it.
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')
    # Short teaser for the homepage's portrait cards.
    description = models.TextField(blank=True, default='')
    # Small label above the card title, e.g. "Locals / Kenya".
    tag = models.CharField(max_length=60, blank=True, default='')
    image = models.ForeignKey(ImageAsset, null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    # The destination places (parks, beaches, towns) the area covers; counted on its card.
    places = models.ManyToManyField('Place', related_name='areas', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.parent.name} › {self.name}' if self.parent_id else self.name

    def descendant_ids(self) -> list:
        ids = [self.id]
        for child in self.children.all():
            ids += child.descendant_ids()
        return ids


class Difficulty(models.TextChoices):
    EASY = 'easy', 'Easy'
    MODERATE = 'moderate', 'Moderate'
    CHALLENGING = 'challenging', 'Challenging'


class Tour(PublishableModel):
    """A bookable package: a Kenyan getaway, an international holiday or a safari."""

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=140, unique=True)
    category = models.ForeignKey(TourCategory, on_delete=models.PROTECT, related_name='tours')
    summary = models.CharField(max_length=300)
    description = models.TextField()

    price_from = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    price_basis = models.CharField(max_length=40, default='per person')

    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    group_size_max = models.PositiveIntegerField(default=12)
    difficulty = models.CharField(max_length=12, choices=Difficulty.choices, default=Difficulty.EASY)

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)

    destination = models.ForeignKey(Destination, null=True, blank=True, on_delete=models.SET_NULL, related_name='tours')
    countries = models.ManyToManyField(Country, related_name='tours', blank=True)
    areas = models.ManyToManyField(TravelArea, related_name='tours', blank=True)
    # The display line from the original cards, e.g. "Diani, Coast" or "4-Country Circuit".
    location_label = models.CharField(max_length=80, blank=True, default='')

    highlights = models.JSONField(default=list, blank=True)
    inclusions = models.JSONField(default=list, blank=True)
    exclusions = models.JSONField(default=list, blank=True)
    # [{day, title, description, activities[], meals[], accommodation}]
    itinerary = models.JSONField(default=list, blank=True)

    hero_image = models.ForeignKey(ImageAsset, on_delete=models.PROTECT, related_name='+')
    gallery = models.ManyToManyField(ImageAsset, through='TourImage', related_name='+', blank=True)

    featured = models.BooleanField(default=False, db_index=True)
    best_selling = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    seo = models.JSONField(null=True, blank=True)

    # Safaris
    parks = models.JSONField(default=list, blank=True)
    game_drive_count = models.PositiveIntegerField(null=True, blank=True)
    conservancy_fees_included = models.BooleanField(null=True, blank=True)

    # Packages and holidays
    departs_from = models.CharField(max_length=120, blank=True, default='')
    departure_dates = models.JSONField(default=list, blank=True)
    visa_support = models.BooleanField(null=True, blank=True)
    flights_included = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-featured', 'order', '-created_at']
        indexes = [models.Index(fields=['status', 'featured', 'order'])]

    def __str__(self):
        return self.title


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageAsset, on_delete=models.PROTECT)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [models.UniqueConstraint(fields=['tour', 'image'], name='unique_tour_gallery_image')]
