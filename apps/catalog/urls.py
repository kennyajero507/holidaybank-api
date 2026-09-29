from django.urls import path

from apps.common.crud import build_views

from . import views
from .resources import categories, destinations, tours

urlpatterns = [
    path('categories', views.CategoryTreeView.as_view()),
    path('countries', views.CountryListView.as_view()),
    path('areas', views.AreaTreeView.as_view()),
    # Before the generic tours routes so "<slug>/related" is not read as a slug.
    path('tours/<str:slug>/related', views.RelatedToursView.as_view()),
    *build_views(tours),
    *build_views(destinations),
    *build_views(categories),
]
