from django.contrib import admin

from .models import Country, Destination, Place, Tour, TourCategory, TourImage, TravelArea


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'iso_code', 'order')
    list_filter = ('region',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kind', 'status', 'order')
    list_filter = ('kind', 'status')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TravelArea)
class TravelAreaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tag', 'status', 'order')
    list_filter = ('status', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('places',)


class PlaceInline(admin.StackedInline):
    model = Place
    extra = 0


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'status', 'featured', 'is_sample', 'order')
    list_filter = ('status', 'featured', 'is_sample', 'country__region')
    search_fields = ('name', 'tagline')
    inlines = [PlaceInline]


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 0


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_from', 'currency', 'duration_days', 'status', 'featured', 'is_sample')
    list_filter = ('status', 'category', 'currency', 'featured', 'best_selling', 'is_sample')
    search_fields = ('title', 'summary')
    filter_horizontal = ('countries', 'areas')
    inlines = [TourImageInline]
