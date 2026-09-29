from django.db.models import Count, Q

from apps.accounts.auth import PublicView
from apps.common.exceptions import ApiError
from apps.common.responses import send

from .models import Country, Tour, TourCategory, TravelArea
from .resources import area_shape, category_shape, country_shape, tour_queryset, tour_shape


class CategoryTreeView(PublicView):
    """
    Published product lines as a tree, with how many published tours each
    holds. The site's navigation and the tour filters are built from this, so
    adding a category in the dashboard adds it to the menu.
    """

    def get(self, request):
        counts = dict(
            Tour.objects.filter(status='published').values('category_id').annotate(n=Count('id')).values_list('category_id', 'n')
        )
        rows = list(TourCategory.objects.filter(status='published').select_related('parent', 'hero_image'))
        by_parent: dict = {}
        for row in rows:
            by_parent.setdefault(row.parent_id, []).append(row)

        def build(node):
            children = [build(child) for child in sorted(by_parent.get(node.id, []), key=lambda c: (c.order, c.name))]
            shape = category_shape(node, children)
            shape['tourCount'] = counts.get(node.id, 0) + sum(c['tourCount'] for c in children)
            return shape

        roots = sorted(by_parent.get(None, []), key=lambda c: (c.order, c.name))
        return send([build(root) for root in roots])


class AreaTreeView(PublicView):
    """
    Published travel areas as a tree (Kenyan > Diani, Maasai Mara...), each
    with how many published tours it holds. A tour can be in several areas of
    one group, so a group counts distinct tours rather than summing children.
    """

    def get(self, request):
        tours_by_area: dict = {}
        links = Tour.areas.through.objects.filter(tour__status='published').values_list('travelarea_id', 'tour_id')
        for area_id, tour_id in links:
            tours_by_area.setdefault(area_id, set()).add(tour_id)

        rows = list(
            TravelArea.objects.filter(status='published')
            .select_related('parent', 'image')
            .annotate(place_count=Count('places', distinct=True))
        )
        by_parent: dict = {}
        for row in rows:
            by_parent.setdefault(row.parent_id, []).append(row)

        def build(node) -> tuple[dict, set]:
            tours = set(tours_by_area.get(node.id, ()))
            children = []
            for child in sorted(by_parent.get(node.id, []), key=lambda c: (c.order, c.name)):
                shape, child_tours = build(child)
                children.append(shape)
                tours |= child_tours
            shape = area_shape(node, children)
            shape['tourCount'] = len(tours)
            return shape, tours

        roots = sorted(by_parent.get(None, []), key=lambda c: (c.order, c.name))
        return send([build(root)[0] for root in roots])


class CountryListView(PublicView):
    """Every country with a count of published tours, for filters and destination tabs."""

    def get(self, request):
        rows = Country.objects.annotate(
            tour_count=Count('tours', filter=Q(tours__status='published'), distinct=True)
        ).order_by('order', 'name')
        data = []
        for c in rows:
            shape = country_shape(c)
            shape['tourCount'] = c.tour_count
            data.append(shape)
        return send(data)


class RelatedToursView(PublicView):
    """Up to three published tours in the same category, then sharing a country."""

    def get(self, request, slug):
        current = Tour.objects.filter(slug=slug, status='published').prefetch_related('countries').first()
        if current is None:
            raise ApiError.not_found('We could not find that tour.')

        base = tour_queryset().filter(status='published').exclude(pk=current.pk)
        picks = list(base.filter(category_id=current.category_id).order_by('-featured', 'order')[:3])
        if len(picks) < 3:
            country_ids = [c.id for c in current.countries.all()]
            more = (
                base.filter(countries__in=country_ids)
                .exclude(pk__in=[p.pk for p in picks])
                .distinct()
                .order_by('-featured', 'order')[: 3 - len(picks)]
            )
            picks += list(more)
        if len(picks) < 3 and current.category.parent_id:
            siblings = (
                base.filter(category__parent_id=current.category.parent_id)
                .exclude(pk__in=[p.pk for p in picks])
                .order_by('-featured', 'order')[: 3 - len(picks)]
            )
            picks += list(siblings)
        return send([tour_shape(t) for t in picks])
