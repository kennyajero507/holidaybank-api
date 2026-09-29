import copy
import re

from django.db import transaction
from rest_framework import serializers

from apps.accounts.auth import AdminView, PublicView
from apps.catalog.models import Destination, TourCategory, TravelArea
from apps.common.responses import send
from apps.common.revalidate import revalidate
from apps.common.validation import OptionalImageSchema, validate
from apps.media.models import ImageAsset
from apps.media.services import image_shape, resolve_image

from .defaults import SITE_SETTINGS_DEFAULTS
from .models import SiteSettings


def get_settings() -> SiteSettings:
    """The one settings row, created with defaults on first read."""
    defaults = {attr: copy.deepcopy(SITE_SETTINGS_DEFAULTS.get(wire)) for wire, attr in SiteSettings.SECTIONS.items()}
    defaults = {k: v for k, v in defaults.items() if v is not None}
    row, _ = SiteSettings.objects.get_or_create(key='primary', defaults=defaults)
    return row


def _collect_urls(value, found: set) -> None:
    if isinstance(value, dict):
        if isinstance(value.get('url'), str):
            found.add(value['url'])
        for item in value.values():
            _collect_urls(item, found)
    elif isinstance(value, list):
        for item in value:
            _collect_urls(item, found)


def _with_credits(value, assets: dict):
    """Adds each image's credit from the media library; alt text stays as edited here."""
    if isinstance(value, dict):
        out = {k: _with_credits(v, assets) for k, v in value.items()}
        asset = assets.get(value.get('url')) if isinstance(value.get('url'), str) else None
        if asset is not None and 'alt' in value:
            shape = image_shape(asset)
            for key in ('credit', 'sourceUrl'):
                if key in shape:
                    out[key] = shape[key]
        return out
    if isinstance(value, list):
        return [_with_credits(item, assets) for item in value]
    return value


def settings_shape(row: SiteSettings) -> dict:
    data = row.as_dict()
    urls: set = set()
    _collect_urls(data, urls)
    assets = {a.url: a for a in ImageAsset.objects.filter(url__in=urls)}
    data = _with_credits(data, assets)
    # Sections added in a later release read as their defaults until saved.
    for wire, value in data.items():
        if value in (None, {}, []) and SITE_SETTINGS_DEFAULTS.get(wire) not in (None, {}, []):
            if wire not in ('socials', 'video'):
                data[wire] = copy.deepcopy(SITE_SETTINGS_DEFAULTS[wire])
    data['id'] = str(row.id)
    data['_id'] = str(row.id)
    data['updatedAt'] = row.updated_at
    return data


class CtaSchema(serializers.Serializer):
    label = serializers.CharField(max_length=60, required=False, allow_blank=True)
    href = serializers.CharField(max_length=200, required=False, allow_blank=True)


class HeroSchema(serializers.Serializer):
    eyebrow = serializers.CharField(max_length=80, required=False, allow_blank=True)
    title = serializers.CharField(max_length=160, required=False)
    subtitle = serializers.CharField(max_length=400, required=False, allow_blank=True)
    backgroundImage = OptionalImageSchema(required=False)
    primaryCta = CtaSchema(required=False)
    secondaryCta = CtaSchema(required=False)


class ValueSchema(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    description = serializers.CharField(max_length=400)
    icon = serializers.CharField(max_length=40, required=False, allow_blank=True)
    image = OptionalImageSchema(required=False, allow_null=True)


class ContactSchema(serializers.Serializer):
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    whatsapp = serializers.CharField(max_length=40, required=False, allow_blank=True)
    email = serializers.CharField(max_length=160, required=False, allow_blank=True)
    addressLine = serializers.CharField(max_length=200, required=False, allow_blank=True)
    poBox = serializers.CharField(max_length=80, required=False, allow_blank=True)
    city = serializers.CharField(max_length=120, required=False, allow_blank=True)
    supportHours = serializers.CharField(max_length=160, required=False, allow_blank=True)


class SocialsSchema(serializers.Serializer):
    facebook = serializers.CharField(max_length=200, required=False, allow_blank=True)
    instagram = serializers.CharField(max_length=200, required=False, allow_blank=True)
    x = serializers.CharField(max_length=200, required=False, allow_blank=True)
    youtube = serializers.CharField(max_length=200, required=False, allow_blank=True)
    tiktok = serializers.CharField(max_length=200, required=False, allow_blank=True)


class NewsletterSchema(serializers.Serializer):
    heading = serializers.CharField(max_length=120, required=False, allow_blank=True)
    blurb = serializers.CharField(max_length=400, required=False, allow_blank=True)


class VideoSchema(serializers.Serializer):
    youtubeId = serializers.RegexField(
        r'^([A-Za-z0-9_-]{11})?$',
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': 'Enter the 11-character YouTube video ID (the v= part of the URL), not the whole link.'
        },
    )


class SeoSchema(serializers.Serializer):
    defaultTitle = serializers.CharField(max_length=70, required=False, allow_blank=True)
    defaultDescription = serializers.CharField(max_length=200, required=False, allow_blank=True)
    ogImage = serializers.CharField(max_length=500, required=False, allow_blank=True)


class NoticeSchema(serializers.Serializer):
    enabled = serializers.BooleanField(required=False)
    text = serializers.CharField(max_length=200, required=False, allow_blank=True)


def _validate_href(value: str) -> None:
    """A path on this site or a full web, mail or phone link; never javascript: and the like."""
    if value.startswith('/') and not value.startswith('//'):
        return
    if re.match(r'^(https?://|mailto:|tel:)\S+$', value):
        return
    raise serializers.ValidationError('Use a path on this site, such as /tours, or a full https:// address.')


class NavImageSchema(serializers.Serializer):
    url = serializers.CharField(max_length=500)
    # Thumbnails sit beside the link text, which already names them, so they
    # are decorative and alt text is optional here.
    alt = serializers.CharField(max_length=300, required=False, allow_blank=True, default='')


class NavLinkSchema(serializers.Serializer):
    id = serializers.CharField(max_length=40)
    label = serializers.CharField(max_length=40, error_messages={'blank': 'Every menu item needs a title.'})
    href = serializers.CharField(max_length=200, validators=[_validate_href], error_messages={'blank': 'Every menu item needs a link.'})
    visible = serializers.BooleanField(default=True)
    image = NavImageSchema(required=False, allow_null=True)


NAV_SOURCES = {
    'category': TourCategory,
    'area': TravelArea,
    'destination': Destination,
}


class NavSourceSchema(serializers.Serializer):
    """A live link to a catalogue record; the web app derives the route and dropdown from it."""

    type = serializers.ChoiceField(choices=list(NAV_SOURCES))
    slug = serializers.CharField(max_length=120)

    def validate(self, attrs):
        if not NAV_SOURCES[attrs['type']].objects.filter(slug=attrs['slug']).exists():
            raise serializers.ValidationError({'slug': f'There is no {attrs["type"]} "{attrs["slug"]}".'})
        return attrs


class NavItemSchema(serializers.Serializer):
    """
    A top-level entry. Either a plain link (label + href + hand-made children)
    or linked to a category, travel area or destination (`source`), in which
    case a blank label inherits the record's name and the route and dropdown
    are derived from the live catalogue when the menu is rendered.

    Thumbnails belong to dropdown links only, so there is no image here.
    """

    id = serializers.CharField(max_length=40)
    label = serializers.CharField(max_length=40, required=False, allow_blank=True, default='')
    href = serializers.CharField(max_length=200, required=False, allow_blank=True, default='', validators=[_validate_href])
    visible = serializers.BooleanField(default=True)
    source = NavSourceSchema(required=False, allow_null=True, default=None)
    # Linked items only: whether the derived dropdown (sub-categories, areas) is shown.
    showChildren = serializers.BooleanField(default=True)
    children = serializers.ListField(child=NavLinkSchema(), required=False, default=list, max_length=12)

    def validate(self, attrs):
        if attrs.get('source'):
            return attrs
        errors = {}
        if not attrs.get('label', '').strip():
            errors['label'] = 'Every menu item needs a title.'
        if not attrs.get('href'):
            errors['href'] = 'Every menu item needs a link.'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class UpdateSettingsBody(serializers.Serializer):
    hero = HeroSchema(required=False)
    heroSlides = serializers.ListField(child=OptionalImageSchema(), required=False, max_length=12)
    values = serializers.ListField(child=ValueSchema(), required=False, max_length=12)
    contact = ContactSchema(required=False)
    socials = SocialsSchema(required=False)
    newsletter = NewsletterSchema(required=False)
    footerBlurb = serializers.CharField(max_length=600, required=False, allow_blank=True)
    video = VideoSchema(required=False)
    seo = SeoSchema(required=False)
    notice = NoticeSchema(required=False)
    # Free-form page copy; validated for shape only.
    promo = serializers.DictField(required=False)
    about = serializers.DictField(required=False)
    home = serializers.DictField(required=False)
    pages = serializers.DictField(required=False)
    brand = serializers.DictField(required=False)
    # Replaced whole on save; an empty list returns the site to the automatic menu.
    navigation = serializers.ListField(child=NavItemSchema(), required=False, max_length=10)


def _register_images(value) -> None:
    """Every {url, alt} inside settings gets a media-library record, so its credit is tracked."""
    if isinstance(value, dict):
        if isinstance(value.get('url'), str) and value.get('url') and 'alt' in value:
            resolve_image(value)
        for item in value.values():
            _register_images(item)
    elif isinstance(value, list):
        for item in value:
            _register_images(item)


class SettingsView(PublicView):
    def get(self, request):
        return send(settings_shape(get_settings()))


class AdminSettingsView(AdminView):
    required_permissions = 'settings.edit'

    def get(self, request):
        return send(settings_shape(get_settings()))

    def patch(self, request):
        body = validate(UpdateSettingsBody, request.data)
        with transaction.atomic():
            row = SiteSettings.objects.select_for_update().get(pk=get_settings().pk)
            for wire, value in body.items():
                attr = SiteSettings.SECTIONS[wire]
                current = getattr(row, attr)
                # Merge per top-level section, so saving one field never wipes its siblings.
                if isinstance(value, dict) and isinstance(current, dict):
                    setattr(row, attr, {**current, **value})
                else:
                    setattr(row, attr, value)
            row.save()
            _register_images({k: v for k, v in body.items() if k != 'brand'})
        revalidate(['settings', 'home'])
        return send(settings_shape(row))
