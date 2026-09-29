"""
Default site-settings content.

Copy marked [source] is taken verbatim, or near-verbatim, from the company's
original website (the prototype index.html). Everything else is supporting
copy written for this build and can be edited in the dashboard.

Contact details: the original site listed "+254 700 000 000" and
hello@holidaybankexpeditions.com. The footer notice states how prices are
quoted and can be edited or switched off in the dashboard.
"""

IMG = '/images'

SITE_SETTINGS_DEFAULTS = {
    'brand': {
        'name': 'Holidaybank Expeditions',  # [source]
        'tagline': 'Travel in Style',  # [source] from the logo
        'logo': {'url': '/brand/logo.svg', 'alt': 'Holidaybank Expeditions: Travel in Style'},
        'logoCompact': {'url': '/brand/logo-compact.svg', 'alt': 'Holidaybank Expeditions'},
        'logoOnLight': {'url': '/brand/logo-on-light.svg', 'alt': 'Holidaybank Expeditions: Travel in Style'},
        'mark': {'url': '/brand/logo-mark.svg', 'alt': 'Holidaybank Expeditions'},
    },
    'hero': {
        'eyebrow': 'Feel The Experience',  # [source]
        'title': "Discover East Africa's Wild Beauty",  # [source]
        'subtitle': (  # [source]
            'Kenyan getaways, safari adventures across East Africa, and handpicked international '
            'escapes — planned by people who know the road, the reserve, and the runway.'
        ),
        'backgroundImage': {'url': f'{IMG}/naivasha-hippo-shoreline.jpg', 'alt': 'A hippo grazing on the shore of Lake Naivasha'},
        'primaryCta': {'label': 'Explore Safaris', 'href': '/tours?category=safaris'},  # [source]
        'secondaryCta': {'label': 'View Kenyan Packages', 'href': '/tours?category=kenyan-packages'},  # [source]
    },
    # The nine subjects of the original hero, in their original order, re-shot in
    # high-resolution landscape Pexels photos (the originals were small and unconfirmed).
    'heroSlides': [
        {'url': f'{IMG}/naivasha-hippo-shoreline.jpg', 'alt': 'A hippo grazing on the shore of Lake Naivasha'},
        {'url': f'{IMG}/ol-pejeta-ranger-rhinos.jpg', 'alt': 'A ranger watching over rhinos at Ol Pejeta'},
        {'url': f'{IMG}/diani-beach-parasols.jpg', 'alt': 'Palm trees and parasols along the white sand of the Kenyan coast'},
        {'url': f'{IMG}/tsavo-red-elephants-river.jpg', 'alt': 'Red-dusted elephants wading through a river in Tsavo'},
        {'url': f'{IMG}/santorini-oia-domes.jpg', 'alt': 'Blue-domed churches above the caldera in Oia, Santorini'},
        {'url': f'{IMG}/mara-leopard-tree.jpg', 'alt': 'A leopard resting on a branch in the Maasai Mara'},
        {'url': f'{IMG}/nairobi-giraffe-city.jpg', 'alt': 'A giraffe in Nairobi National Park with the city skyline beyond'},
        {'url': f'{IMG}/paris-eiffel-seine.jpg', 'alt': 'The Eiffel Tower above the Seine'},
        {'url': f'{IMG}/mombasa-beach-sunrise.jpg', 'alt': 'People silhouetted on a Mombasa beach at sunrise'},
    ],
    # Each value restates something the original site says about the company.
    'values': [
        {
            'title': 'People who know the way',
            'description': 'Planned from Nairobi around your dates, who is travelling and what you want to spend.',
            'icon': 'compass',
            'image': {'url': f'{IMG}/ol-pejeta-rhinos-game-drive.jpg', 'alt': 'A safari vehicle beside grazing rhinos'},
        },
        {
            'title': 'Timed to the migration',
            'description': 'Every safari is built around the migration calendar and your budget.',
            'icon': 'clock',
            'image': {'url': f'{IMG}/mara-zebra-river-crossing.jpg', 'alt': 'Zebra crossing the Mara River'},
        },
        {
            'title': 'Visas and flights sorted',
            'description': 'Curated routes across Europe with the visa paperwork and flights arranged for you.',
            'icon': 'receipt',
            'image': {'url': f'{IMG}/paris-eiffel-tower.jpg', 'alt': 'The Eiffel Tower in Paris'},
        },
        {
            'title': 'Built around your budget',
            'description': 'Tell us roughly what you want to spend and we will plan the trip to fit it.',
            'icon': 'leaf',
            'image': {'url': f'{IMG}/diani-beach-palms.jpg', 'alt': 'Diani Beach at midday'},
        },
    ],
    'contact': {
        'phone': '+254 700 000 000',  # [source] placeholder number on the original site
        'whatsapp': '',
        'email': 'hello@holidaybankexpeditions.com',  # [source]
        'addressLine': '',
        'poBox': '',
        'city': 'Nairobi, Kenya',  # [source]
        'supportHours': 'Tell us your dates and budget and we will come back with options',
    },
    'socials': {},
    'newsletter': {
        'heading': 'Travel notes',
        'blurb': 'Occasional updates on new packages, safari seasons and European departures.',
    },
    'footerBlurb': (  # [source]
        'Holidaybank Expeditions plans Kenyan getaways, East African safaris, and international '
        'travel for people who want it done properly.'
    ),
    # Empty until an administrator adds the company's own film.
    'video': {},
    'seo': {
        'defaultTitle': 'Holidaybank Expeditions',
        'defaultDescription': (
            'Kenyan getaways, safari adventures across East Africa, and handpicked international '
            'escapes, planned from Nairobi.'
        ),
        'ogImage': f'{IMG}/mara-leopard-branch.jpg',
    },
    'promo': {
        'eyebrow': 'Safaris',
        'title': 'Follow the herds across the border.',
        # Written for this build. The original's line ("From a weekend in the Mara...") is the
        # Safaris section intro on the same page, so repeating it here read as a copy error.
        'body': (
            'Mara River crossings from July to October, the Serengeti across the border, and gorilla '
            'treks in Uganda and Rwanda. Tell us your month and we will match the route to the herds.'
        ),
        'cta': {'label': 'See safari packages', 'href': '/tours?category=safaris'},
        'image': {'url': f'{IMG}/mara-wildebeest-migration.jpg', 'alt': 'Wildebeest climbing out of a riverbed in the Maasai Mara'},
    },
    'about': {
        'title': 'About Holidaybank Expeditions',
        'intro': 'Travel in Style',
        'heading': 'Kenyan getaways, East African safaris and international travel',
        'paragraphs': [
            # [source] footer description, and the three product lines from the navigation.
            'Holidaybank Expeditions plans Kenyan getaways, East African safaris, and international '
            'travel for people who want it done properly.',
            'For travellers at home in Kenya there are weekend escapes and longer breaks across the '
            'country, built for locals who want the best of it without the guesswork. For wildlife, '
            'there are safaris from a weekend in the Mara to a full circuit across Kenya, Tanzania, '
            'Uganda and Rwanda. And for travellers ready to go further, there are curated routes '
            'across Europe with visas and flights sorted.',
            'We are based in Nairobi. Tell us where you would like to go, when, and roughly what you '
            'want to spend, and we will plan the trip around it.',
        ],
        'images': [
            {'url': f'{IMG}/nairobi-giraffe-skyline.jpg', 'alt': 'A giraffe with the Nairobi skyline behind'},
            {'url': f'{IMG}/santorini-oia-lane.jpg', 'alt': 'A flower-lined lane in Oia, Santorini'},
        ],
        'pillars': [
            {'title': 'Kenyan Packages', 'eyebrow': 'Locals', 'href': '/tours?category=kenyan-packages',
             'body': "Weekend escapes and longer breaks across Kenya, built for locals who want the country's best without the guesswork."},
            {'title': 'Safaris', 'eyebrow': 'Kenya · Tanzania · Uganda · Rwanda', 'href': '/tours?category=safaris',
             'body': 'From a weekend in the Mara to a full circuit across four countries, built around the migration calendar and your budget.'},
            {'title': 'International', 'eyebrow': 'Europe', 'href': '/tours?category=international',
             'body': 'Curated routes across Europe, visas and flights sorted, for travellers ready to go further.'},
        ],
    },
    'home': {
        'packagesEyebrow': 'Hand-picked',
        'packagesTitle': 'Popular packages',
        'destinationsEyebrow': 'Where we go',
        'destinationsTitle': 'From the Mara to the Mediterranean',
        'testimonialsImage': {'url': f'{IMG}/mara-cheetah.jpg', 'alt': 'A cheetah looking back over its shoulder in the Maasai Mara'},
        'ctaTitle': 'Tell us where you want to go',
        'ctaBody': 'Share your dates, who is travelling and a rough budget, and we will put the options together.',
        'ctaImage': {'url': f'{IMG}/zanzibar-boats-sunset.jpg', 'alt': 'Boats moored off a palm-lined Zanzibar shore at sunset'},
    },
    # Banner copy and imagery for each top-level page.
    'pages': {
        'tours': {
            'title': 'Packages & Safaris',
            'subtitle': 'Kenyan getaways, safari adventures across East Africa, and handpicked international escapes.',
            'image': {'url': f'{IMG}/mara-leopard-tree.jpg', 'alt': 'A leopard resting on a branch in the Maasai Mara'},
        },
        'destinations': {
            'title': 'Where we travel',
            'subtitle': 'Four East African countries for safaris and getaways, and five European ones for city breaks and rail journeys.',
            'image': {'url': f'{IMG}/amboseli-elephant-kilimanjaro.jpg', 'alt': 'An elephant with Kilimanjaro behind'},
        },
        'services': {
            'title': 'What we do',
            'subtitle': 'Holiday packages, safaris and international trips, with the logistics handled.',
            'image': {'url': f'{IMG}/ol-pejeta-ranger-rhinos.jpg', 'alt': 'A ranger watching over rhinos at Ol Pejeta'},
        },
        'about': {
            'title': 'About Holidaybank Expeditions',
            'subtitle': 'Travel in Style',
            'image': {'url': f'{IMG}/nairobi-giraffe-city.jpg', 'alt': 'A giraffe in Nairobi National Park with the city skyline beyond'},
        },
        'contact': {
            'title': 'Plan your trip',
            'subtitle': 'Tell us where, when and who is travelling, and we will come back with options.',
            'image': {'url': f'{IMG}/mombasa-beach-sunrise.jpg', 'alt': 'People silhouetted on a Mombasa beach at sunrise'},
        },
        'blog': {
            'title': 'Travel Journal',
            'subtitle': 'Planning guides for Kenya, East African safaris and Europe.',
            'image': {'url': f'{IMG}/santorini-oia-domes.jpg', 'alt': 'Blue-domed churches above the caldera in Oia, Santorini'},
        },
        'credits': {
            'title': 'Photo credits',
            'subtitle': 'Where every photograph on this site comes from.',
            'image': {'url': f'{IMG}/swiss-alps-red-train.jpg', 'alt': 'A red train crossing the Swiss Alps'},
        },
    },
    # Footer notice on how prices are quoted.
    'notice': {'enabled': True, 'text': 'Prices are per person and subject to availability at the time of booking.'},
    # Empty: the web app builds the menu from the category tree until an admin
    # arranges one under Navigation menu.
    'navigation': [],
}
