"""
Countries, categories, destinations and tours.

WHAT COMES FROM WHERE
---------------------
The original Holidaybank website (prototype index.html) lists 17 packages in
four groups. For each of those, the title, place label, card description and
"from" price are copied exactly, and durations are taken from the description
where it states one ("Three nights", "Fourteen days"...). Everything else about
those packages (itineraries, inclusions, group sizes) was drafted for this
build from the card description, and each tour's `source_note` says so.

Tours with `is_sample: True` do not exist on the original site at all. They
fill out the catalogue for demonstration and are flagged in the dashboard.

Ratings and review counts are zero throughout: the original site shows none,
and invented review scores would be a false claim.
"""

ORIGINAL_NOTE = (
    'Title, place, description and price from the original website. Itinerary, inclusions and '
    'group size drafted for this build; confirm before launch.'
)
SAMPLE_NOTE = 'Demo package created for this build; not on the original website.'
DESTINATION_NOTE = 'Destination copy written for this build around the packages on the original website.'

COUNTRIES = [
    {'name': 'Kenya', 'slug': 'kenya', 'iso_code': 'KE', 'region': 'east-africa', 'order': 1},
    {'name': 'Tanzania', 'slug': 'tanzania', 'iso_code': 'TZ', 'region': 'east-africa', 'order': 2},
    {'name': 'Uganda', 'slug': 'uganda', 'iso_code': 'UG', 'region': 'east-africa', 'order': 3},
    {'name': 'Rwanda', 'slug': 'rwanda', 'iso_code': 'RW', 'region': 'east-africa', 'order': 4},
    {'name': 'France', 'slug': 'france', 'iso_code': 'FR', 'region': 'europe', 'order': 10},
    {'name': 'Greece', 'slug': 'greece', 'iso_code': 'GR', 'region': 'europe', 'order': 11},
    {'name': 'Italy', 'slug': 'italy', 'iso_code': 'IT', 'region': 'europe', 'order': 12},
    {'name': 'Switzerland', 'slug': 'switzerland', 'iso_code': 'CH', 'region': 'europe', 'order': 13},
    {'name': 'Spain', 'slug': 'spain', 'iso_code': 'ES', 'region': 'europe', 'order': 14},
]

# The original navigation: Kenyan Packages > Locals, International > Europe,
# Safaris > Kenyan Safaris / Kenya · Tanzania · Uganda · Rwanda. Section copy
# (eyebrow and description) is the original's own.
CATEGORIES = [
    {
        'slug': 'kenyan-packages', 'name': 'Kenyan Packages', 'kind': 'local', 'order': 1,
        'eyebrow': 'Locals', 'nav_label': 'Kenyan Packages',
        'description': "Weekend escapes and longer breaks across Kenya, built for locals who want the country's best without the guesswork.",
        'image': 'diani-beach-parasols.jpg',
    },
    {
        'slug': 'locals', 'parent': 'kenyan-packages', 'name': 'Locals', 'kind': 'local', 'order': 1,
        'eyebrow': 'Kenyan Packages', 'nav_label': 'Locals',
        'description': "Weekend escapes and longer breaks across Kenya, built for locals who want the country's best without the guesswork.",
        'image': 'naivasha-hippo-shoreline.jpg',
    },
    {
        'slug': 'international', 'name': 'International', 'kind': 'international', 'order': 2,
        'eyebrow': 'International · Europe', 'nav_label': 'International',
        'description': 'Curated routes across Europe, visas and flights sorted, for travellers ready to go further.',
        'image': 'santorini-oia-domes.jpg',
    },
    {
        'slug': 'europe', 'parent': 'international', 'name': 'Europe', 'kind': 'international', 'order': 1,
        'eyebrow': 'International', 'nav_label': 'Europe',
        'description': 'Curated routes across Europe, visas and flights sorted, for travellers ready to go further.',
        'image': 'paris-eiffel-seine.jpg',
    },
    {
        'slug': 'safaris', 'name': 'Safaris', 'kind': 'safari', 'order': 3,
        'eyebrow': 'Safaris', 'nav_label': 'Safaris',
        'description': 'From a weekend in the Mara to a full circuit across four countries — every safari is built around the migration calendar and your budget.',
        'image': 'mara-leopard-tree.jpg',
    },
    {
        'slug': 'kenyan-safaris', 'parent': 'safaris', 'name': 'Kenyan Safaris', 'kind': 'safari', 'order': 1,
        'eyebrow': 'Safaris', 'nav_label': 'Kenyan Safaris',
        'description': 'Game drives in the Maasai Mara, Amboseli and Tsavo, from a weekend to a week.',
        'image': 'tsavo-red-elephants-river.jpg',
    },
    {
        'slug': 'east-africa-safaris', 'parent': 'safaris', 'name': 'Kenya · Tanzania · Uganda · Rwanda', 'kind': 'safari',
        'order': 2, 'eyebrow': 'Safaris', 'nav_label': 'Kenya · Tanzania · Uganda · Rwanda',
        'description': 'Cross-border safaris: the Mara–Serengeti migration, and gorilla trekking in Uganda and Rwanda.',
        'image': 'serengeti-zebra-wildebeest.jpg',
    },
]

DESTINATIONS = [
    {
        'country': 'Kenya', 'name': 'Kenya', 'slug': 'kenya', 'order': 1, 'featured': True,
        'category_label': 'East Africa',
        'tagline': 'The Mara, Amboseli and the coast.',
        'overview': (
            'Kenya is where Holidaybank is based and where most trips begin. In a single week you can '
            'follow the herds across the Maasai Mara, watch elephants beneath Kilimanjaro in Amboseli, '
            'and finish on the white sand at Diani. For residents it is also the easiest escape there '
            'is: a weekend at Lake Naivasha, a day among the giraffes in Nairobi, or a few nights on '
            'the coast.'
        ),
        'hero': 'mara-wildebeest-migration.jpg', 'card': 'mara-leopard-branch.jpg',
        'highlights': [
            'The Great Migration in the Maasai Mara, usually July to October',
            'Elephants against Kilimanjaro in Amboseli',
            'Red-dust elephants and Mzima Springs in Tsavo',
            'Diani Beach on the south coast',
            'Rhinos at Ol Pejeta Conservancy',
        ],
        'best_time': {'months': ['January', 'February', 'July', 'August', 'September', 'October'],
                      'note': 'The long dry season (July to October) brings the migration to the Mara. January and February are dry, warm and quieter.'},
        'places': [
            {'name': 'Maasai Mara', 'kind': 'National reserve', 'image': 'mara-wildebeest-migration.jpg', 'best_time': 'July – October',
             'blurb': "Kenya's best-known reserve, and the northern end of the wildebeest migration.",
             'highlights': ['Mara River crossings', 'Big cats year-round', 'Maasai village visits']},
            {'name': 'Amboseli', 'kind': 'National park', 'image': 'amboseli-elephant-kilimanjaro.jpg', 'best_time': 'June – October',
             'blurb': 'Large elephant herds with Kilimanjaro rising behind them on clear mornings.',
             'highlights': ['Elephant herds', 'Kilimanjaro views', 'Swamp birdlife']},
            {'name': 'Tsavo East & West', 'kind': 'National parks', 'image': 'tsavo-red-elephants.jpg', 'best_time': 'June – October',
             'blurb': "Kenya's largest park, famed for red-dust elephants and the Mzima Springs hippo pools.",
             'highlights': ['Red elephants', 'Mzima Springs', 'Lava flows at Shetani']},
            {'name': 'Diani Beach', 'kind': 'Beach', 'image': 'diani-beach-palms.jpg', 'best_time': 'December – March',
             'blurb': "White sand south of Mombasa, with reef snorkelling and dhow cruises.",
             'highlights': ['Reef snorkelling', 'Sunset dhow cruises', 'Colobus monkeys in the coastal forest']},
            {'name': 'Watamu & Malindi', 'kind': 'Beach', 'image': 'kenya-coast-sunset.jpg', 'best_time': 'December – March',
             'blurb': 'The coast north of Mombasa: Watamu Marine National Park and the Swahili old town of Malindi.',
             'highlights': ['Watamu Marine National Park', 'Gede Ruins', 'Malindi old town']},
            {'name': 'Lake Naivasha', 'kind': 'Lake', 'image': 'naivasha-hippos-pelicans.jpg', 'best_time': 'Year-round',
             'blurb': 'A freshwater lake in the Rift Valley with hippos, pelicans and a walking safari on Crescent Island.',
             'highlights': ['Boat rides among hippos', 'Crescent Island walking safari', "Hell's Gate nearby"]},
            {'name': 'Nairobi', 'kind': 'City', 'image': 'nairobi-giraffe-skyline.jpg', 'best_time': 'Year-round',
             'blurb': 'The capital, with a national park inside the city limits.',
             'highlights': ['Elephant orphanage', 'Giraffe Centre', 'Nairobi National Park']},
            {'name': 'Nanyuki & Ol Pejeta', 'kind': 'Conservancy', 'image': 'ol-pejeta-rhinos-game-drive.jpg', 'best_time': 'Year-round',
             'blurb': 'Rhino conservation on the equator, with Mt. Kenya on the horizon.',
             'highlights': ['Rhino sanctuary', 'Equator crossing', 'Mt. Kenya views']},
            {'name': 'Lake Nakuru', 'kind': 'National park', 'image': 'nakuru-flamingo-flight.jpg', 'best_time': 'Year-round',
             'blurb': 'A Rift Valley soda lake known for flamingos, pelicans and rhinos.',
             'highlights': ['Flamingos and pelicans', 'Rhinos', "Baboon Cliff viewpoint"]},
        ],
    },
    {
        'country': 'Tanzania', 'name': 'Tanzania', 'slug': 'tanzania', 'order': 2, 'featured': True,
        'category_label': 'East Africa',
        'tagline': 'The Serengeti, the crater, and the Spice Island.',
        'overview': (
            "Across the border from the Mara, the Serengeti holds the migration for most of the year. "
            'Holidaybank pairs it with the Mara on migration safaris, and with the Ngorongoro Crater '
            'and Zanzibar for longer trips.'
        ),
        'hero': 'serengeti-zebra-wildebeest.jpg', 'card': 'ngorongoro-crater-landscape.jpg',
        'highlights': ['The Serengeti migration', 'The Ngorongoro Crater floor', 'Beaches and Stone Town on Zanzibar'],
        'best_time': {'months': ['January', 'February', 'June', 'July', 'August', 'September', 'October'],
                      'note': 'June to October for dry-season game viewing; January and February for calving in the southern Serengeti.'},
        'places': [
            {'name': 'Serengeti', 'kind': 'National park', 'image': 'serengeti-zebra-wildebeest.jpg', 'best_time': 'June – October',
             'blurb': 'Endless plains and the bulk of the migration for much of the year.',
             'highlights': ['The migration', 'Big cats', 'Balloon flights']},
            {'name': 'Ngorongoro Crater', 'kind': 'Conservation area', 'image': 'ngorongoro-crater-landscape.jpg', 'best_time': 'Year-round',
             'blurb': 'A collapsed volcano whose floor holds a dense concentration of wildlife.',
             'highlights': ['Crater-floor game drive', 'Black rhino', 'Crater-rim views']},
            {'name': 'Zanzibar', 'kind': 'Island', 'image': 'zanzibar-dhow-beach.jpg', 'best_time': 'June – October, December – February',
             'blurb': 'White beaches and Stone Town, a natural end to a safari.',
             'highlights': ['Stone Town', 'Dhow sailing', 'Spice tours']},
        ],
    },
    {
        'country': 'Uganda', 'name': 'Uganda', 'slug': 'uganda', 'order': 3,
        'category_label': 'East Africa',
        'tagline': 'Gorillas in Bwindi, chimpanzees in Kibale.',
        'overview': (
            "Uganda's two signature encounters are gorilla trekking in Bwindi Impenetrable Forest and "
            'chimpanzee tracking in Kibale. Permits are limited, so these trips are planned well ahead.'
        ),
        'hero': 'gorilla-uganda-resting.jpg', 'card': 'gorilla-bwindi-feeding.jpg',
        'highlights': ['Mountain gorilla trekking', 'Chimpanzee tracking', 'Crater lakes around Fort Portal'],
        'best_time': {'months': ['June', 'July', 'August', 'December', 'January', 'February'],
                      'note': 'Treks run all year; the drier months make forest trails easier underfoot.'},
        'places': [
            {'name': 'Bwindi Impenetrable Forest', 'kind': 'National park', 'image': 'gorilla-bwindi-foliage.jpg', 'best_time': 'June – August, December – February',
             'blurb': 'Steep rainforest home to habituated mountain gorilla families.',
             'highlights': ['Gorilla trekking', 'Forest walks', 'Community visits']},
            {'name': 'Kibale Forest', 'kind': 'National park', 'image': None, 'best_time': 'Year-round',
             'blurb': 'Tropical forest known for chimpanzee tracking.',
             'highlights': ['Chimpanzee tracking', 'Primate walks', 'Bigodi wetland']},
        ],
    },
    {
        'country': 'Rwanda', 'name': 'Rwanda', 'slug': 'rwanda', 'order': 4,
        'category_label': 'East Africa',
        'tagline': 'Volcanoes, gorillas and Lake Kivu.',
        'overview': (
            'Volcanoes National Park, in the Virunga foothills, is a short drive from Kigali and one of '
            'the most accessible places to trek to mountain gorillas. Lake Kivu makes a quiet place to '
            'rest afterwards.'
        ),
        'hero': 'gorilla-rwanda-forest.jpg', 'card': 'gorilla-silverback-rwanda.jpg',
        'highlights': ['Gorilla trekking in Volcanoes National Park', 'Lake Kivu', 'Kigali'],
        'best_time': {'months': ['June', 'July', 'August', 'September', 'December', 'January', 'February'],
                      'note': 'The long dry season (June to September) is the most popular time to trek.'},
        'places': [
            {'name': 'Volcanoes National Park', 'kind': 'National park', 'image': 'gorilla-kinigi-habitat.jpg', 'best_time': 'June – September',
             'blurb': 'Bamboo and cloud forest on the slopes of the Virunga volcanoes.',
             'highlights': ['Gorilla trekking', 'Golden monkeys', 'Virunga views']},
            {'name': 'Lake Kivu', 'kind': 'Lake', 'image': None, 'best_time': 'Year-round',
             'blurb': 'A deep, calm lake on the border with the DRC, lined with small resort towns.',
             'highlights': ['Boat trips', 'Lakeside stays', 'Coffee farms']},
        ],
    },
    {
        'country': 'France', 'name': 'France', 'slug': 'france', 'order': 10, 'featured': True,
        'category_label': 'Europe',
        'tagline': 'The Louvre, the Seine and the 7th arrondissement.',
        'overview': (
            "Holidaybank's Paris city break stays in the 7th arrondissement, near the Eiffel Tower, "
            'with a Seine dinner cruise and skip-the-line Louvre access. Paris is also the first stop on '
            'the Grand European Tour.'
        ),
        'hero': 'paris-eiffel-seine.jpg', 'card': 'paris-eiffel-tower.jpg',
        'highlights': ['The Louvre', 'A Seine dinner cruise', 'The Eiffel Tower'],
        'best_time': {'months': ['April', 'May', 'June', 'September', 'October'],
                      'note': 'Spring and early autumn are mild and less crowded than midsummer.'},
        'places': [
            {'name': 'Paris', 'kind': 'City', 'image': 'paris-eiffel-tower.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'Museums, river cruises and neighbourhoods best seen on foot.',
             'highlights': ['Louvre', 'Seine cruise', 'Montmartre']},
        ],
    },
    {
        'country': 'Greece', 'name': 'Greece', 'slug': 'greece', 'order': 11, 'featured': True,
        'category_label': 'Europe',
        'tagline': 'Caldera views and the Acropolis.',
        'overview': (
            'Holidaybank combines Athens and Santorini: the Acropolis and the city first, then '
            'caldera-view suites in Oia and a sunset sail. Greece is also on the Grand European Tour.'
        ),
        'hero': 'athens-parthenon-visitors.jpg', 'card': 'santorini-oia-lane.jpg',
        'highlights': ['Caldera-view stays in Oia', 'The Acropolis', 'Catamaran sunset sail'],
        'best_time': {'months': ['May', 'June', 'September', 'October'],
                      'note': 'Warm seas without the peak-season crowds of July and August.'},
        'places': [
            {'name': 'Santorini', 'kind': 'Island', 'image': 'santorini-oia-lane.jpg', 'best_time': 'May – October',
             'blurb': 'Whitewashed villages on the rim of a flooded caldera.',
             'highlights': ['Oia sunsets', 'Caldera sailing', 'Volcanic beaches']},
            {'name': 'Athens', 'kind': 'City', 'image': 'athens-acropolis.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'The Acropolis and the Plaka, with the sea a short ride away.',
             'highlights': ['Acropolis tour', 'Plaka', 'Acropolis Museum']},
        ],
    },
    {
        'country': 'Italy', 'name': 'Italy', 'slug': 'italy', 'order': 12, 'featured': True,
        'category_label': 'Europe',
        'tagline': 'Rome, Florence and Venice by rail.',
        'overview': (
            "A ten-day rail route through Italy's three signature cities, with a Tuscan food tour "
            'included. Italy is also on the Grand European Tour.'
        ),
        'hero': 'venice-grand-canal.jpg', 'card': 'rome-colosseum.jpg',
        'highlights': ['The Colosseum and Vatican', 'A Tuscan food tour', 'Venice canals'],
        'best_time': {'months': ['April', 'May', 'June', 'September', 'October'],
                      'note': 'Shoulder seasons are best for walking the cities.'},
        'places': [
            {'name': 'Rome', 'kind': 'City', 'image': 'rome-colosseum.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'Ancient Rome, the Vatican and long lunches.',
             'highlights': ['Colosseum', 'Vatican Museums', 'Trastevere']},
            {'name': 'Florence', 'kind': 'City', 'image': 'florence-duomo-dusk.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'Renaissance art and the gateway to Tuscany.',
             'highlights': ['The Duomo', 'Uffizi Gallery', 'Tuscan food tour']},
            {'name': 'Venice', 'kind': 'City', 'image': 'venice-canal-bridge.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'Canals, bridges and St Mark’s Square.',
             'highlights': ['Grand Canal', "St Mark's Basilica", 'Gondola ride']},
        ],
    },
    {
        'country': 'Switzerland', 'name': 'Switzerland', 'slug': 'switzerland', 'order': 13,
        'category_label': 'Europe',
        'tagline': 'Scenic trains and the Matterhorn.',
        'overview': (
            'Scenic-train travel through Interlaken and Zermatt, with a Matterhorn cable-car ride. '
            'Switzerland is also on the Grand European Tour.'
        ),
        'hero': 'swiss-bernina-express.jpg', 'card': 'zermatt-matterhorn.jpg',
        'highlights': ['Scenic rail journeys', 'The Matterhorn', 'Interlaken lakes'],
        'best_time': {'months': ['June', 'July', 'August', 'September', 'December', 'January', 'February'],
                      'note': 'Summer for lakes and hiking; winter for snow.'},
        'places': [
            {'name': 'Interlaken', 'kind': 'Mountain town', 'image': 'swiss-alps-red-train.jpg', 'best_time': 'June – September',
             'blurb': 'Between two lakes, with mountain railways in every direction.',
             'highlights': ['Lake cruises', 'Mountain railways', 'Jungfrau region']},
            {'name': 'Zermatt', 'kind': 'Mountain town', 'image': 'zermatt-matterhorn-autumn.jpg', 'best_time': 'Year-round',
             'blurb': 'A car-free village at the foot of the Matterhorn.',
             'highlights': ['Matterhorn cable car', 'Gornergrat railway', 'Alpine walks']},
        ],
    },
    {
        'country': 'Spain', 'name': 'Spain', 'slug': 'spain', 'order': 14,
        'category_label': 'Europe',
        'tagline': 'Gaudí, tapas and Toledo.',
        'overview': (
            'Gaudí architecture, tapas trails, and a day trip to Toledo, on flexible seven or ten-day '
            'routes through Barcelona and Madrid.'
        ),
        'hero': 'madrid-plaza-mayor.jpg', 'card': 'barcelona-sagrada-familia.jpg',
        'highlights': ['The Sagrada Família', 'Tapas trails', 'A day trip to Toledo'],
        'best_time': {'months': ['March', 'April', 'May', 'September', 'October', 'November'],
                      'note': 'Spring and autumn avoid the heat of an inland summer.'},
        'places': [
            {'name': 'Barcelona', 'kind': 'City', 'image': 'barcelona-sagrada-familia.jpg', 'best_time': 'April – June, September – October',
             'blurb': 'Gaudí, the Gothic Quarter and the Mediterranean.',
             'highlights': ['Sagrada Família', 'Park Güell', 'Gothic Quarter']},
            {'name': 'Madrid', 'kind': 'City', 'image': 'madrid-plaza-mayor.jpg', 'best_time': 'March – May, September – November',
             'blurb': "Spain's capital: galleries, plazas and late dinners.",
             'highlights': ['Plaza Mayor', 'Prado Museum', 'Tapas trail']},
            {'name': 'Toledo', 'kind': 'Historic city', 'image': None, 'best_time': 'March – May, September – November',
             'blurb': 'A walled hilltop city an easy day trip from Madrid.',
             'highlights': ['Cathedral', 'Old town walls', 'Alcázar']},
        ],
    },
]


def day(n, title, description, activities=(), meals=(), accommodation=''):
    return {'day': n, 'title': title, 'description': description, 'activities': list(activities),
            'meals': list(meals), 'accommodation': accommodation}


B, L, D = 'Breakfast', 'Lunch', 'Dinner'

LOCAL_EXCLUSIONS = ['Travel insurance', 'Tips and personal expenses', 'Drinks unless stated']
INTL_EXCLUSIONS = ['Travel insurance', 'Meals not listed', 'Tips and personal expenses', 'City tourist taxes paid locally']
SAFARI_EXCLUSIONS = ['International flights', 'Travel insurance', 'Visas', 'Tips for guides and camp staff', 'Drinks unless stated']

TOURS = [
    # ------------------------------------------------------------------
    # Kenyan Packages > Locals  (original)
    # ------------------------------------------------------------------
    {
        'title': 'Diani Beach Escape', 'category': 'locals', 'location_label': 'Diani, Coast',
        'summary': "Three nights on Kenya's whitest sand, with a sunset dhow cruise and reef snorkelling included.",
        'price_from': 24500, 'currency': 'KES', 'days': 4, 'nights': 3, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'diani-beach-parasols.jpg', 'gallery': ['kenya-coast-sunset.jpg', 'zanzibar-fishing-boat.jpg'],
        'featured': True, 'best_selling': True, 'order': 1, 'group_size_max': 20, 'departs_from': 'Diani (own travel), or with SGR/flight add-on from Nairobi',
        'description': (
            "Three nights on Diani's white sand south of Mombasa. The package is built around the beach: "
            'a sunset dhow cruise along the coast and a morning snorkelling the reef are included, and the '
            'rest of the time is yours.'
        ),
        'highlights': ['Three nights beside Diani Beach', 'Sunset dhow cruise', 'Reef snorkelling trip'],
        'inclusions': ['3 nights beachfront accommodation', 'Daily breakfast', 'Sunset dhow cruise', 'Guided reef snorkelling with equipment', 'Resort transfers within Diani'],
        'exclusions': ['Travel to Diani (SGR or flight can be added)', *LOCAL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Diani', 'Check in and settle on the beach.', ['Hotel check-in', 'Free afternoon on the beach'], [D], 'Beachfront hotel, Diani'),
            day(2, 'Reef snorkelling', 'A morning boat trip to the reef, afternoon free.', ['Guided snorkelling on the reef'], [B], 'Beachfront hotel, Diani'),
            day(3, 'Sunset dhow cruise', 'A free day, then out on a traditional dhow as the sun goes down.', ['Sunset dhow cruise'], [B, D], 'Beachfront hotel, Diani'),
            day(4, 'Departure', 'Breakfast and check-out.', [], [B]),
        ],
    },
    {
        'title': 'Lake Naivasha Weekend', 'category': 'locals', 'location_label': 'Naivasha',
        'summary': 'Boat rides among hippos, a Crescent Island walking safari, and a cliffside lodge stay.',
        'price_from': 15900, 'currency': 'KES', 'days': 3, 'nights': 2, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'naivasha-hippo-shoreline.jpg', 'gallery': ['naivasha-greater-flamingos.jpg', 'mara-giraffes.jpg'],
        'featured': True, 'best_selling': True, 'order': 2, 'group_size_max': 14, 'departs_from': 'Nairobi',
        'description': (
            'A Rift Valley weekend two hours from Nairobi: a boat ride among the hippos, a walking safari '
            'on Crescent Island among giraffe and zebra, and two nights at a cliffside lodge above the lake.'
        ),
        'highlights': ['Boat ride among hippos', 'Crescent Island walking safari', 'Cliffside lodge stay'],
        'inclusions': ['Return road transport from Nairobi', '2 nights cliffside lodge', 'Full board', 'Lake boat ride', 'Crescent Island entry and guided walk'],
        'exclusions': LOCAL_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to Naivasha', 'Drive down the escarpment into the Rift Valley and check in.', ['Rift Valley viewpoint stop', 'Lodge check-in'], [L, D], 'Cliffside lodge, Naivasha'),
            day(2, 'Hippos and Crescent Island', 'Out on the lake in the morning, then a guided walk on Crescent Island.', ['Boat ride among hippos', 'Crescent Island walking safari'], [B, L, D], 'Cliffside lodge, Naivasha'),
            day(3, 'Return to Nairobi', 'A slow breakfast and the drive back.', [], [B]),
        ],
    },
    {
        'title': 'Nairobi City & Nature', 'category': 'locals', 'location_label': 'Nairobi',
        'summary': 'The elephant orphanage, giraffe centre, and rooftop dining — a full day of the capital done right.',
        'price_from': 8200, 'currency': 'KES', 'days': 1, 'nights': 0, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'nairobi-giraffe-city.jpg', 'gallery': ['nairobi-np-giraffe.jpg', 'mara-elephant-savanna.jpg'],
        'featured': True, 'order': 3, 'group_size_max': 12, 'departs_from': 'Your Nairobi hotel or home',
        'description': (
            "A full day of the capital: the elephant orphanage's morning visit, feeding giraffes at the "
            'Giraffe Centre, and dinner on a rooftop as the city lights come on.'
        ),
        'highlights': ['Elephant orphanage visit', 'Giraffe Centre', 'Rooftop dinner'],
        'inclusions': ['Pick-up and drop-off in Nairobi', 'Elephant orphanage entry', 'Giraffe Centre entry', 'Lunch', 'Rooftop dinner'],
        'exclusions': LOCAL_EXCLUSIONS,
        'itinerary': [
            day(1, 'A day in Nairobi', 'Orphanage in the morning, giraffes after lunch, rooftop dinner to finish.',
                ['Elephant orphanage visit', 'Giraffe Centre', 'Rooftop dinner'], [L, D]),
        ],
    },
    {
        'title': 'Nanyuki & Ol Pejeta', 'category': 'locals', 'location_label': 'Mt. Kenya Region',
        'summary': 'Rhino sanctuary visits and equator-line stops, with views of Mt. Kenya on clear mornings.',
        'price_from': 19000, 'currency': 'KES', 'days': 3, 'nights': 2, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'ol-pejeta-ranger-rhinos.jpg', 'gallery': ['mara-herd-safari.jpg', 'lodge-veranda.jpg'],
        'order': 4, 'group_size_max': 14, 'departs_from': 'Nairobi',
        'description': (
            'North to Nanyuki for rhino sanctuary visits at Ol Pejeta and a stop on the equator line, '
            'with Mt. Kenya on the skyline on clear mornings.'
        ),
        'highlights': ['Ol Pejeta rhino sanctuary', 'Equator-line stop', 'Mt. Kenya views'],
        'inclusions': ['Return road transport from Nairobi', '2 nights accommodation near Nanyuki', 'Full board', 'Ol Pejeta conservancy fees', 'Game drives'],
        'exclusions': LOCAL_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to Nanyuki', 'Drive north past the equator and check in.', ['Equator-line stop', 'Afternoon game drive'], [L, D], 'Lodge near Nanyuki'),
            day(2, 'Ol Pejeta', 'A full day in the conservancy, including the rhino sanctuary.', ['Rhino sanctuary visit', 'Game drives'], [B, L, D], 'Lodge near Nanyuki'),
            day(3, 'Return to Nairobi', 'Early views of Mt. Kenya, then the drive home.', [], [B]),
        ],
    },
    # ------------------------------------------------------------------
    # International > Europe  (original)
    # ------------------------------------------------------------------
    {
        'title': 'Paris City Break', 'category': 'europe', 'location_label': 'France',
        'summary': 'Five nights in the 7th arrondissement, a Seine dinner cruise, and skip-the-line Louvre access.',
        'price_from': 1650, 'currency': 'USD', 'days': 6, 'nights': 5, 'countries': ['France'], 'destination': 'france',
        'image': 'paris-eiffel-seine.jpg', 'gallery': [], 'featured': True, 'best_selling': True, 'order': 10,
        'group_size_max': 16, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': (
            'Five nights in the 7th arrondissement, within walking distance of the Eiffel Tower, with a '
            'dinner cruise on the Seine and skip-the-line entry to the Louvre. Schengen visa paperwork '
            'and flights are arranged for you.'
        ),
        'highlights': ['Hotel in the 7th arrondissement', 'Seine dinner cruise', 'Skip-the-line Louvre access'],
        'inclusions': ['5 nights hotel in the 7th arrondissement', 'Daily breakfast', 'Seine dinner cruise', 'Skip-the-line Louvre entry', 'Airport transfers in Paris', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Paris', 'Transfer to the hotel in the 7th.', ['Airport transfer'], [], 'Hotel, 7th arrondissement'),
            day(2, 'The Louvre', 'Skip-the-line entry in the morning; the afternoon is free.', ['Louvre visit'], [B], 'Hotel, 7th arrondissement'),
            day(3, 'Free day', 'Explore at your own pace.', [], [B], 'Hotel, 7th arrondissement'),
            day(4, 'Seine dinner cruise', 'A free day ending on the river.', ['Seine dinner cruise'], [B, D], 'Hotel, 7th arrondissement'),
            day(5, 'Free day', 'Montmartre, the Marais or the shops.', [], [B], 'Hotel, 7th arrondissement'),
            day(6, 'Departure', 'Transfer to the airport.', ['Airport transfer'], [B]),
        ],
    },
    {
        'title': 'Santorini & Athens', 'category': 'europe', 'location_label': 'Greece',
        'summary': 'Caldera-view suites in Oia, an Acropolis tour, and a private catamaran sunset sail.',
        'price_from': 1890, 'currency': 'USD', 'days': 7, 'nights': 6, 'countries': ['Greece'], 'destination': 'greece',
        'image': 'santorini-oia-domes.jpg', 'gallery': ['athens-acropolis.jpg', 'athens-parthenon-columns.jpg'],
        'featured': True, 'best_selling': True, 'order': 11, 'group_size_max': 12, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': (
            'Athens first, with a guided tour of the Acropolis, then over to Santorini for caldera-view '
            'suites in Oia and a private catamaran sail at sunset.'
        ),
        'highlights': ['Caldera-view suite in Oia', 'Guided Acropolis tour', 'Private catamaran sunset sail'],
        'inclusions': ['2 nights hotel in Athens', '4 nights caldera-view suite in Oia', 'Daily breakfast', 'Guided Acropolis tour', 'Private catamaran sunset sail', 'Athens–Santorini ferry or flight', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Athens', 'Transfer to the hotel.', ['Airport transfer'], [], 'Hotel, Athens'),
            day(2, 'The Acropolis', 'A guided morning on the Acropolis and the Plaka.', ['Guided Acropolis tour'], [B], 'Hotel, Athens'),
            day(3, 'To Santorini', 'Ferry or short flight to Santorini and on to Oia.', ['Transfer to Oia'], [B], 'Caldera-view suite, Oia'),
            day(4, 'Oia', 'A free day on the caldera.', [], [B], 'Caldera-view suite, Oia'),
            day(5, 'Catamaran sunset sail', 'A private sail around the caldera at sunset.', ['Private catamaran sail'], [B, D], 'Caldera-view suite, Oia'),
            day(6, 'Free day', 'Beaches, wineries or the walk to Fira.', [], [B], 'Caldera-view suite, Oia'),
            day(7, 'Departure', 'Transfer for the flight home.', [], [B]),
        ],
    },
    {
        'title': 'Rome, Florence & Venice', 'category': 'europe', 'location_label': 'Italy',
        'summary': "A ten-day rail route through Italy's three signature cities, with a Tuscan food tour included.",
        'price_from': 2450, 'currency': 'USD', 'days': 10, 'nights': 9, 'countries': ['Italy'], 'destination': 'italy',
        'image': 'rome-colosseum.jpg', 'gallery': ['florence-duomo-skyline.jpg', 'venice-grand-canal.jpg', 'venice-canal-bridge.jpg'],
        'order': 12, 'group_size_max': 16, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': (
            "Ten days by rail through Rome, Florence and Venice, Italy's three signature cities, with a "
            'Tuscan food tour included along the way.'
        ),
        'highlights': ['High-speed rail between the three cities', 'Tuscan food tour', 'Colosseum, Duomo and Grand Canal'],
        'inclusions': ['9 nights hotels (3 per city)', 'Daily breakfast', 'Rail tickets Rome–Florence–Venice', 'Tuscan food tour', 'Arrival and departure transfers', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Rome', 'Transfer to the hotel.', ['Airport transfer'], [], 'Hotel, Rome'),
            day(2, 'Ancient Rome', 'The Colosseum and Forum.', ['Colosseum and Forum'], [B], 'Hotel, Rome'),
            day(3, 'Rome at leisure', 'The Vatican, Trastevere or a free day.', [], [B], 'Hotel, Rome'),
            day(4, 'Train to Florence', 'High-speed rail north to Florence.', ['Rail to Florence'], [B], 'Hotel, Florence'),
            day(5, 'Tuscan food tour', 'A day out in the Tuscan countryside with tastings.', ['Tuscan food tour'], [B, L], 'Hotel, Florence'),
            day(6, 'Florence', 'The Duomo and the Uffizi.', [], [B], 'Hotel, Florence'),
            day(7, 'Train to Venice', 'Rail to Venice and a first evening on the canals.', ['Rail to Venice'], [B], 'Hotel, Venice'),
            day(8, 'Venice', "St Mark's Square and the Grand Canal.", [], [B], 'Hotel, Venice'),
            day(9, 'Venice at leisure', 'Murano, Burano or a gondola.', [], [B], 'Hotel, Venice'),
            day(10, 'Departure', 'Transfer to the airport.', ['Airport transfer'], [B]),
        ],
    },
    {
        'title': 'Swiss Alps Rail Journey', 'category': 'europe', 'location_label': 'Switzerland',
        'summary': 'Scenic-train travel through Interlaken and Zermatt, with a Matterhorn cable-car ride.',
        'price_from': 2780, 'currency': 'USD', 'days': 8, 'nights': 7, 'countries': ['Switzerland'], 'destination': 'switzerland',
        'image': 'zermatt-matterhorn-lake.jpg', 'gallery': ['swiss-alps-red-train.jpg', 'swiss-bernina-express.jpg', 'zermatt-matterhorn-autumn.jpg'],
        'order': 13, 'group_size_max': 14, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': 'Scenic-train travel through Interlaken and Zermatt, with a Matterhorn cable-car ride.',
        'highlights': ['Scenic train legs', 'Interlaken lakes', 'Matterhorn cable-car ride'],
        'inclusions': ['7 nights hotels in Interlaken and Zermatt', 'Daily breakfast', 'Swiss rail pass for the route', 'Matterhorn cable-car ticket', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Zurich', 'Train to Interlaken.', ['Rail to Interlaken'], [], 'Hotel, Interlaken'),
            day(2, 'Interlaken', 'Lake cruise and time in town.', ['Lake cruise'], [B], 'Hotel, Interlaken'),
            day(3, 'Mountain railways', 'A day on the Jungfrau region railways.', ['Mountain rail excursion'], [B], 'Hotel, Interlaken'),
            day(4, 'Interlaken at leisure', 'Free day.', [], [B], 'Hotel, Interlaken'),
            day(5, 'Scenic train to Zermatt', 'Across the Alps by rail.', ['Scenic rail to Zermatt'], [B], 'Hotel, Zermatt'),
            day(6, 'The Matterhorn', 'Cable car up for views of the Matterhorn.', ['Matterhorn cable car'], [B], 'Hotel, Zermatt'),
            day(7, 'Zermatt at leisure', 'Walks in the car-free village.', [], [B], 'Hotel, Zermatt'),
            day(8, 'Departure', 'Rail back to the airport.', [], [B]),
        ],
    },
    {
        'title': 'Barcelona & Madrid', 'category': 'europe', 'location_label': 'Spain',
        'summary': 'Gaudí architecture, tapas trails, and a day trip to Toledo — flexible seven or ten-day options.',
        'price_from': 1540, 'currency': 'USD', 'days': 7, 'nights': 6, 'countries': ['Spain'], 'destination': 'spain',
        'image': 'barcelona-sagrada-aerial.jpg', 'gallery': ['madrid-plaza-mayor.jpg'],
        'order': 14, 'group_size_max': 16, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': (
            'Barcelona for Gaudí and the Gothic Quarter, then Madrid for tapas trails and a day trip to '
            'Toledo. Choose the seven-day route shown here or a ten-day version with more time in each city.'
        ),
        'highlights': ['Gaudí architecture', 'Tapas trails', 'Day trip to Toledo', 'Seven or ten-day options'],
        'inclusions': ['6 nights hotels in Barcelona and Madrid', 'Daily breakfast', 'Rail Barcelona–Madrid', 'Toledo day trip', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Barcelona', 'Transfer to the hotel.', ['Airport transfer'], [], 'Hotel, Barcelona'),
            day(2, 'Gaudí', 'The Sagrada Família and Park Güell.', ['Gaudí architecture tour'], [B], 'Hotel, Barcelona'),
            day(3, 'Barcelona at leisure', 'The Gothic Quarter and the beach.', [], [B], 'Hotel, Barcelona'),
            day(4, 'Train to Madrid', 'High-speed rail to Madrid; tapas in the evening.', ['Rail to Madrid', 'Tapas trail'], [B], 'Hotel, Madrid'),
            day(5, 'Toledo', 'A day trip to the walled city of Toledo.', ['Toledo day trip'], [B], 'Hotel, Madrid'),
            day(6, 'Madrid', 'The Prado and Plaza Mayor.', [], [B], 'Hotel, Madrid'),
            day(7, 'Departure', 'Transfer to the airport.', [], [B]),
        ],
    },
    {
        'title': 'Grand European Tour', 'category': 'europe', 'location_label': 'Multi-country',
        'summary': 'Eighteen days across France, Switzerland, Italy and Greece — our most complete route.',
        'price_from': 4200, 'currency': 'USD', 'days': 18, 'nights': 17, 'countries': ['France', 'Switzerland', 'Italy', 'Greece'],
        'destination': None, 'image': 'venice-grand-canal.jpg',
        'gallery': ['paris-eiffel-tower.jpg', 'zermatt-matterhorn.jpg', 'rome-colosseum.jpg', 'santorini-oia-lane.jpg'],
        'featured': True, 'order': 15, 'group_size_max': 16, 'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': (
            'Eighteen days across France, Switzerland, Italy and Greece: Paris, the Swiss Alps, Rome, '
            'Florence and Venice, finishing in the Greek islands. The most complete route we offer.'
        ),
        'highlights': ['Four countries in eighteen days', 'Paris, the Alps, Italy and the Greek islands', 'Visa and flights arranged'],
        'inclusions': ['17 nights hotels', 'Daily breakfast', 'Rail and internal flights between countries', 'Selected guided tours', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Paris', 'Arrive and settle in.', ['Airport transfer'], [], 'Hotel, Paris'),
            day(4, 'To the Swiss Alps', 'Rail from Paris to Switzerland.', ['Rail to Switzerland'], [B], 'Hotel, Interlaken'),
            day(7, 'To Italy', 'Rail over the Alps to Italy.', ['Rail to Venice'], [B], 'Hotel, Venice'),
            day(9, 'Florence', 'Rail south to Florence.', [], [B], 'Hotel, Florence'),
            day(11, 'Rome', 'Rail to Rome.', [], [B], 'Hotel, Rome'),
            day(14, 'To Greece', 'Fly to Athens.', ['Flight to Athens'], [B], 'Hotel, Athens'),
            day(15, 'Santorini', 'On to the islands.', ['Transfer to Santorini'], [B], 'Hotel, Santorini'),
            day(18, 'Departure', 'Fly home from Athens.', [], [B]),
        ],
    },
    # ------------------------------------------------------------------
    # Safaris > Kenyan Safaris  (original)
    # ------------------------------------------------------------------
    {
        'title': 'Maasai Mara, 3 Days', 'category': 'kenyan-safaris', 'location_label': 'Narok County',
        'summary': 'Two game drives daily in the reserve, a Maasai village visit, and a tented-camp stay.',
        'price_from': 650, 'currency': 'USD', 'days': 3, 'nights': 2, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'mara-leopard-tree.jpg', 'gallery': ['mara-lions-stalking.jpg', 'mara-cheetah.jpg', 'maasai-jumping-dance.jpg', 'camp-white-tents.jpg'],
        'featured': True, 'best_selling': True, 'order': 20, 'group_size_max': 7, 'departs_from': 'Nairobi',
        'parks': ['Maasai Mara National Reserve'], 'game_drive_count': 4, 'conservancy_fees_included': True, 'difficulty': 'easy',
        'description': (
            'Two game drives a day in the Maasai Mara, a visit to a Maasai village, and two nights in a '
            'tented camp. The classic short safari from Nairobi.'
        ),
        'highlights': ['Two game drives daily', 'Maasai village visit', 'Tented-camp stay'],
        'inclusions': ['Return transport from Nairobi in a safari vehicle', '2 nights tented camp', 'Full board', 'Park fees', 'Game drives with a driver-guide', 'Maasai village visit'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to the Mara', 'Drive to the reserve for an afternoon game drive.', ['Afternoon game drive'], [L, D], 'Tented camp, Maasai Mara'),
            day(2, 'Full day in the Mara', 'Morning and afternoon game drives, with a Maasai village visit.', ['Morning game drive', 'Maasai village visit', 'Afternoon game drive'], [B, L, D], 'Tented camp, Maasai Mara'),
            day(3, 'Return to Nairobi', 'A final early drive, then back to Nairobi.', ['Early morning game drive'], [B, L]),
        ],
    },
    {
        'title': 'Amboseli & Kilimanjaro Views', 'category': 'kenyan-safaris', 'location_label': 'Kajiado County',
        'summary': "Elephant herds against the world's most photographed backdrop, two nights in-park.",
        'price_from': 540, 'currency': 'USD', 'days': 3, 'nights': 2, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'amboseli-elephant-kilimanjaro.jpg', 'gallery': ['amboseli-elephant-mountain.jpg', 'amboseli-elephants-walking.jpg', 'amboseli-elephant-herd-kajiado.jpg'],
        'best_selling': True, 'order': 21, 'group_size_max': 7, 'departs_from': 'Nairobi',
        'parks': ['Amboseli National Park'], 'game_drive_count': 4, 'conservancy_fees_included': True,
        'description': "Elephant herds against Kilimanjaro, the world's most photographed backdrop, with two nights inside the park.",
        'highlights': ['Two nights in-park', 'Elephant herds', 'Kilimanjaro views'],
        'inclusions': ['Return transport from Nairobi', '2 nights in-park lodge', 'Full board', 'Park fees', 'Game drives'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to Amboseli', 'South to Amboseli for an afternoon drive.', ['Afternoon game drive'], [L, D], 'Lodge, Amboseli'),
            day(2, 'Amboseli', 'Early start for the clearest views of Kilimanjaro.', ['Morning game drive', 'Afternoon game drive'], [B, L, D], 'Lodge, Amboseli'),
            day(3, 'Return to Nairobi', 'Morning drive and return.', ['Morning game drive'], [B]),
        ],
    },
    {
        'title': 'Tsavo East & West', 'category': 'kenyan-safaris', 'location_label': 'Taita-Taveta',
        'summary': "Kenya's largest park, famed for red-dust elephants and the Mzima Springs hippo pools.",
        'price_from': 580, 'currency': 'USD', 'days': 4, 'nights': 3, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'tsavo-red-elephants-river.jpg', 'gallery': ['tsavo-elephants-road.jpg', 'tsavo-elephant-field.jpg'],
        'order': 22, 'group_size_max': 7, 'departs_from': 'Nairobi or Mombasa',
        'parks': ['Tsavo East National Park', 'Tsavo West National Park'], 'game_drive_count': 5, 'conservancy_fees_included': True,
        'description': "Both halves of Kenya's largest park: red-dust elephants in Tsavo East, and the Mzima Springs hippo pools in Tsavo West.",
        'highlights': ['Red-dust elephants', 'Mzima Springs hippo pools', 'Both Tsavo parks'],
        'inclusions': ['Transport from Nairobi or Mombasa', '3 nights lodges', 'Full board', 'Park fees', 'Game drives'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'To Tsavo East', 'Travel to Tsavo East for an afternoon drive.', ['Afternoon game drive'], [L, D], 'Lodge, Tsavo East'),
            day(2, 'Tsavo East', 'A full day among the red elephants.', ['Game drives'], [B, L, D], 'Lodge, Tsavo East'),
            day(3, 'Tsavo West and Mzima Springs', 'Cross to Tsavo West and visit Mzima Springs.', ['Mzima Springs', 'Afternoon game drive'], [B, L, D], 'Lodge, Tsavo West'),
            day(4, 'Return', 'Morning drive and departure.', ['Morning game drive'], [B]),
        ],
    },
    # ------------------------------------------------------------------
    # Safaris > Kenya · Tanzania · Uganda · Rwanda  (original)
    # ------------------------------------------------------------------
    {
        'title': 'Mara–Serengeti Migration', 'category': 'east-africa-safaris', 'location_label': 'Kenya + Tanzania',
        'summary': 'Follow the herds across the border — river crossings, big cats, and two ecosystems in one trip.',
        'price_from': 1480, 'currency': 'USD', 'days': 7, 'nights': 6, 'countries': ['Kenya', 'Tanzania'], 'destination': 'tanzania',
        'image': 'mara-wildebeest-migration.jpg', 'gallery': ['mara-zebra-river-crossing.jpg', 'serengeti-wildebeest-grazing.jpg', 'serengeti-lions-resting.jpg'],
        'featured': True, 'best_selling': True, 'order': 30, 'group_size_max': 7, 'departs_from': 'Nairobi',
        'parks': ['Maasai Mara National Reserve', 'Serengeti National Park'], 'game_drive_count': 10, 'conservancy_fees_included': True,
        'description': (
            'Follow the herds across the border: river crossings and big cats in the Maasai Mara, then '
            'into the Serengeti. Two ecosystems in one trip, timed to the migration.'
        ),
        'highlights': ['Mara River crossings (in season)', 'Big cats', 'Two ecosystems in one trip'],
        'inclusions': ['Transport from Nairobi', '6 nights camps and lodges', 'Full board', 'Park fees', 'Game drives', 'Border crossing assistance'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to the Mara', 'Drive to the Mara.', ['Afternoon game drive'], [L, D], 'Tented camp, Maasai Mara'),
            day(2, 'Maasai Mara', 'Full day following the herds.', ['Game drives'], [B, L, D], 'Tented camp, Maasai Mara'),
            day(3, 'Mara River', 'Time at the river for crossings, in season.', ['River crossing watch'], [B, L, D], 'Tented camp, Maasai Mara'),
            day(4, 'Into the Serengeti', 'Cross into Tanzania.', ['Border crossing', 'Game drive en route'], [B, L, D], 'Camp, northern Serengeti'),
            day(5, 'Serengeti', 'Full day in the Serengeti.', ['Game drives'], [B, L, D], 'Camp, Serengeti'),
            day(6, 'Central Serengeti', 'Big cat country around Seronera.', ['Game drives'], [B, L, D], 'Camp, Serengeti'),
            day(7, 'Departure', 'Fly or drive out.', [], [B]),
        ],
    },
    {
        'title': 'Volcanoes NP Gorilla Trek', 'category': 'east-africa-safaris', 'location_label': 'Rwanda',
        'summary': 'A permitted, guided trek to habituated mountain gorilla families in the Virunga foothills.',
        'price_from': 2100, 'currency': 'USD', 'days': 4, 'nights': 3, 'countries': ['Rwanda'], 'destination': 'rwanda',
        'image': 'gorilla-silverback-rwanda.jpg', 'gallery': ['gorilla-kinigi-habitat.jpg'],
        'order': 31, 'group_size_max': 8, 'departs_from': 'Kigali', 'difficulty': 'challenging',
        'parks': ['Volcanoes National Park'], 'game_drive_count': 0, 'conservancy_fees_included': False,
        'description': 'A permitted, guided trek to a habituated mountain gorilla family in the Virunga foothills, from Kigali.',
        'highlights': ['Gorilla trekking permit arranged', 'Guided trek in the Virungas', 'Kigali city visit'],
        'inclusions': ['Airport transfers in Kigali', '3 nights accommodation', 'Full board near the park', 'Gorilla permit arrangement', 'Guided trek'],
        'exclusions': ['Gorilla permit fee (quoted at current park rate)', *SAFARI_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Kigali', 'Transfer and a short city visit.', ['Kigali city visit'], [D], 'Hotel, Kigali'),
            day(2, 'To Volcanoes National Park', 'Drive north to the park.', [], [B, L, D], 'Lodge near Kinigi'),
            day(3, 'Gorilla trek', 'Trek with rangers to a habituated family.', ['Gorilla trek'], [B, L, D], 'Lodge near Kinigi'),
            day(4, 'Return to Kigali', 'Drive back for departure.', [], [B]),
        ],
    },
    {
        'title': 'Bwindi Gorillas & Chimps', 'category': 'east-africa-safaris', 'location_label': 'Uganda',
        'summary': "Gorilla trekking in Bwindi plus chimp tracking in Kibale — Uganda's two signature encounters.",
        'price_from': 1950, 'currency': 'USD', 'days': 6, 'nights': 5, 'countries': ['Uganda'], 'destination': 'uganda',
        'image': 'gorilla-bwindi-feeding.jpg', 'gallery': ['gorilla-bwindi-foliage.jpg', 'gorilla-uganda-forest.jpg'],
        'order': 32, 'group_size_max': 8, 'departs_from': 'Entebbe', 'difficulty': 'challenging',
        'parks': ['Kibale Forest National Park', 'Bwindi Impenetrable National Park'], 'game_drive_count': 0,
        'description': "Uganda's two signature encounters in one trip: chimpanzee tracking in Kibale, then gorilla trekking in Bwindi.",
        'highlights': ['Chimpanzee tracking in Kibale', 'Gorilla trekking in Bwindi', 'Permits arranged'],
        'inclusions': ['Transport from Entebbe', '5 nights accommodation', 'Full board', 'Permit arrangement', 'Guided treks'],
        'exclusions': ['Gorilla and chimpanzee permit fees (quoted at current park rates)', *SAFARI_EXCLUSIONS],
        'itinerary': [
            day(1, 'Entebbe to Kibale', 'Drive west to Kibale.', [], [L, D], 'Lodge, Kibale'),
            day(2, 'Chimpanzee tracking', 'Morning tracking in Kibale Forest.', ['Chimpanzee tracking'], [B, L, D], 'Lodge, Kibale'),
            day(3, 'To Bwindi', 'A long, scenic drive south.', [], [B, L, D], 'Lodge, Bwindi'),
            day(4, 'Gorilla trek', 'Trek with rangers to a habituated family.', ['Gorilla trek'], [B, L, D], 'Lodge, Bwindi'),
            day(5, 'Bwindi', 'Community walk or a rest day.', ['Community walk'], [B, L, D], 'Lodge, Bwindi'),
            day(6, 'Departure', 'Fly or drive back to Entebbe.', [], [B]),
        ],
    },
    {
        'title': 'East Africa Grand Safari', 'category': 'east-africa-safaris', 'location_label': '4-Country Circuit',
        'summary': "Fourteen days: Maasai Mara, Serengeti, gorilla trekking in Uganda, and Rwanda's Lake Kivu.",
        'price_from': 4650, 'currency': 'USD', 'days': 14, 'nights': 13, 'countries': ['Kenya', 'Tanzania', 'Uganda', 'Rwanda'],
        'destination': None, 'image': 'serengeti-zebra-wildebeest.jpg',
        'gallery': ['mara-lioness-cubs.jpg', 'ngorongoro-zebras-grazing.jpg', 'gorilla-uganda-forest.jpg'],
        'featured': True, 'order': 33, 'group_size_max': 7, 'departs_from': 'Nairobi', 'difficulty': 'moderate',
        'parks': ['Maasai Mara National Reserve', 'Serengeti National Park', 'Bwindi Impenetrable National Park', 'Lake Kivu'],
        'game_drive_count': 12,
        'description': (
            "Fourteen days across four countries: the Maasai Mara, the Serengeti, gorilla trekking in "
            "Uganda, and Rwanda's Lake Kivu to finish."
        ),
        'highlights': ['Four countries', 'The Mara and the Serengeti', 'Gorilla trekking', 'Lake Kivu'],
        'inclusions': ['All ground transport and regional flights on the route', '13 nights accommodation', 'Full board on safari', 'Park fees', 'Game drives', 'Permit arrangement'],
        'exclusions': ['Gorilla permit fee (quoted at current park rate)', *SAFARI_EXCLUSIONS],
        'itinerary': [
            day(1, 'Nairobi to the Maasai Mara', 'Start with three nights in the Mara.', ['Game drives'], [L, D], 'Camp, Maasai Mara'),
            day(4, 'Into the Serengeti', 'Cross into Tanzania.', ['Game drives'], [B, L, D], 'Camp, Serengeti'),
            day(7, 'Fly to Uganda', 'Regional flight to Uganda and on to Bwindi.', ['Regional flight'], [B, D], 'Lodge, Bwindi'),
            day(9, 'Gorilla trek', 'Trek with rangers to a habituated family.', ['Gorilla trek'], [B, L, D], 'Lodge, Bwindi'),
            day(11, 'To Rwanda and Lake Kivu', 'Cross into Rwanda for the lake.', [], [B, L, D], 'Lodge, Lake Kivu'),
            day(14, 'Departure from Kigali', 'Transfer to Kigali airport.', [], [B]),
        ],
    },
    # ------------------------------------------------------------------
    # Demo packages (not on the original site)
    # ------------------------------------------------------------------
    {
        'sample': True, 'title': 'Nairobi National Park Morning Drive', 'category': 'locals', 'location_label': 'Nairobi',
        'summary': 'An early game drive in the national park on the edge of the city, back in time for lunch.',
        'price_from': 7500, 'currency': 'KES', 'days': 1, 'nights': 0, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'nairobi-np-giraffe.jpg', 'gallery': [], 'order': 5, 'group_size_max': 7, 'departs_from': 'Your Nairobi hotel or home',
        'description': 'A half-day game drive in Nairobi National Park, starting early when the animals are most active.',
        'highlights': ['Early-morning game drive', 'Giraffe, rhino and buffalo', 'Back by lunchtime'],
        'inclusions': ['Pick-up and drop-off in Nairobi', 'Park entry fees', 'Driver-guide', 'Bottled water'],
        'exclusions': LOCAL_EXCLUSIONS,
        'itinerary': [day(1, 'Morning game drive', 'Pick-up at dawn, four hours in the park, home by lunch.', ['Game drive'], [])],
    },
    {
        'sample': True, 'title': 'Lake Nakuru Flamingo Day Safari', 'category': 'kenyan-safaris', 'location_label': 'Nakuru County',
        'summary': 'A long day trip from Nairobi to the flamingo lake, with rhinos and pelicans along the shore.',
        'price_from': 220, 'currency': 'USD', 'days': 1, 'nights': 0, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'nakuru-flamingo-flock.jpg', 'gallery': ['nakuru-lesser-flamingos.jpg', 'nakuru-pelicans.jpg', 'nakuru-flamingo-group.jpg'],
        'order': 23, 'group_size_max': 7, 'departs_from': 'Nairobi', 'parks': ['Lake Nakuru National Park'], 'game_drive_count': 1,
        'conservancy_fees_included': True,
        'description': 'A full-day trip from Nairobi to Lake Nakuru National Park for flamingos, pelicans and rhinos.',
        'highlights': ['Flamingos and pelicans', 'Rhinos', 'Rift Valley viewpoints'],
        'inclusions': ['Return transport from Nairobi', 'Park fees', 'Game drive', 'Picnic lunch'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [day(1, 'Lake Nakuru', 'Out early, a full game drive around the lake, back by evening.', ['Game drive', 'Baboon Cliff viewpoint'], [L])],
    },
    {
        'sample': True, 'title': 'Mara Balloon Safari Weekend', 'category': 'kenyan-safaris', 'location_label': 'Narok County',
        'summary': 'Two nights in the Mara with a dawn hot-air balloon flight and bush breakfast.',
        'price_from': 890, 'currency': 'USD', 'days': 3, 'nights': 2, 'countries': ['Kenya'], 'destination': 'kenya',
        'image': 'balloon-mara-sunrise.jpg', 'gallery': ['balloon-mara-dawn.jpg', 'balloon-safari-kenya.jpg', 'mara-giraffes.jpg'],
        'order': 24, 'group_size_max': 7, 'departs_from': 'Nairobi', 'parks': ['Maasai Mara National Reserve'], 'game_drive_count': 3,
        'conservancy_fees_included': True,
        'description': 'A Maasai Mara weekend built around a dawn balloon flight over the plains, landing to a bush breakfast.',
        'highlights': ['Dawn balloon flight', 'Bush breakfast', 'Game drives'],
        'inclusions': ['Return transport from Nairobi', '2 nights tented camp', 'Full board', 'Balloon flight with breakfast', 'Park fees'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to the Mara', 'Drive in for an afternoon game drive.', ['Afternoon game drive'], [L, D], 'Tented camp, Maasai Mara'),
            day(2, 'Balloon flight', 'Lift off before sunrise; breakfast where you land.', ['Balloon flight', 'Bush breakfast', 'Afternoon game drive'], [B, L, D], 'Tented camp, Maasai Mara'),
            day(3, 'Return', 'Back to Nairobi.', [], [B, L]),
        ],
    },
    {
        'sample': True, 'title': 'Serengeti & Ngorongoro Crater', 'category': 'east-africa-safaris', 'location_label': 'Northern Tanzania',
        'summary': 'Six days in northern Tanzania: the Serengeti plains and a full morning on the crater floor.',
        'price_from': 2350, 'currency': 'USD', 'days': 6, 'nights': 5, 'countries': ['Tanzania'], 'destination': 'tanzania',
        'image': 'ngorongoro-crater-landscape.jpg', 'gallery': ['ngorongoro-zebras-grazing.jpg', 'ngorongoro-lioness.jpg', 'serengeti-lioness.jpg'],
        'order': 34, 'group_size_max': 7, 'departs_from': 'Arusha', 'parks': ['Serengeti National Park', 'Ngorongoro Conservation Area'],
        'game_drive_count': 8, 'conservancy_fees_included': True,
        'description': 'The Serengeti and the Ngorongoro Crater from Arusha, with time on the crater floor at first light.',
        'highlights': ['Serengeti game drives', 'Ngorongoro Crater floor', 'Starts in Arusha'],
        'inclusions': ['Transport from Arusha', '5 nights lodges and camps', 'Full board', 'Park and crater fees', 'Game drives'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Arusha to the crater rim', 'Drive to the Ngorongoro highlands.', [], [L, D], 'Lodge, Ngorongoro rim'),
            day(2, 'Into the Serengeti', 'Across the plains to the Serengeti.', ['Game drive'], [B, L, D], 'Camp, Serengeti'),
            day(3, 'Serengeti', 'Full day in the park.', ['Game drives'], [B, L, D], 'Camp, Serengeti'),
            day(4, 'Serengeti', 'Another full day following the herds.', ['Game drives'], [B, L, D], 'Camp, Serengeti'),
            day(5, 'Ngorongoro Crater', 'Down onto the crater floor early.', ['Crater-floor game drive'], [B, L, D], 'Lodge, Ngorongoro rim'),
            day(6, 'Return to Arusha', 'Drive back to Arusha.', [], [B]),
        ],
    },
    {
        'sample': True, 'title': 'Safari & Zanzibar Beach', 'category': 'east-africa-safaris', 'location_label': 'Kenya + Zanzibar',
        'summary': 'Three nights in the Mara followed by four nights on a Zanzibar beach.',
        'price_from': 2650, 'currency': 'USD', 'days': 8, 'nights': 7, 'countries': ['Kenya', 'Tanzania'], 'destination': 'tanzania',
        'image': 'zanzibar-boats-sunset.jpg', 'gallery': ['zanzibar-dhow-shore.jpg', 'zanzibar-low-tide-boat.jpg', 'mara-lions-stalking.jpg'],
        'order': 35, 'group_size_max': 7, 'departs_from': 'Nairobi', 'parks': ['Maasai Mara National Reserve', 'Zanzibar'], 'game_drive_count': 5,
        'description': 'A Maasai Mara safari, then a flight to Zanzibar for beach time and Stone Town.',
        'highlights': ['Maasai Mara game drives', 'Zanzibar beach stay', 'Stone Town'],
        'inclusions': ['Transport from Nairobi', 'Nairobi–Zanzibar flight', '3 nights tented camp (full board)', '4 nights beach hotel (half board)', 'Park fees'],
        'exclusions': SAFARI_EXCLUSIONS,
        'itinerary': [
            day(1, 'Nairobi to the Mara', 'Drive to the Mara.', ['Afternoon game drive'], [L, D], 'Tented camp, Maasai Mara'),
            day(2, 'Maasai Mara', 'Full day of game drives.', ['Game drives'], [B, L, D], 'Tented camp, Maasai Mara'),
            day(4, 'Fly to Zanzibar', 'Back to Nairobi and fly to the island.', ['Flight to Zanzibar'], [B, D], 'Beach hotel, Zanzibar'),
            day(6, 'Stone Town', 'A guided walk through the old town.', ['Stone Town walk'], [B, D], 'Beach hotel, Zanzibar'),
            day(8, 'Departure', 'Transfer to the airport.', [], [B]),
        ],
    },
    {
        'sample': True, 'title': 'Florence & Tuscany Short Break', 'category': 'europe', 'location_label': 'Italy',
        'summary': 'Four nights in Florence with a day among Tuscan vineyards.',
        'price_from': 1380, 'currency': 'USD', 'days': 5, 'nights': 4, 'countries': ['Italy'], 'destination': 'italy',
        'image': 'florence-duomo-skyline.jpg', 'gallery': ['florence-duomo-dusk.jpg'], 'order': 16, 'group_size_max': 12,
        'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': 'A shorter Italian trip: four nights in Florence and a day out in the Tuscan countryside.',
        'highlights': ['Four nights in Florence', 'Tuscan vineyard day', 'Uffizi and the Duomo'],
        'inclusions': ['4 nights hotel in Florence', 'Daily breakfast', 'Tuscan countryside day tour', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Florence', 'Transfer to the hotel.', [], [], 'Hotel, Florence'),
            day(2, 'Florence', 'The Duomo and Uffizi.', [], [B], 'Hotel, Florence'),
            day(3, 'Tuscany', 'Vineyards and hill towns.', ['Tuscan day tour'], [B, L], 'Hotel, Florence'),
            day(4, 'Florence at leisure', 'Free day.', [], [B], 'Hotel, Florence'),
            day(5, 'Departure', 'Transfer to the airport.', [], [B]),
        ],
    },
    {
        'sample': True, 'title': 'Madrid & Toledo City Break', 'category': 'europe', 'location_label': 'Spain',
        'summary': "Four nights in Spain's capital with a day trip to Toledo.",
        'price_from': 1190, 'currency': 'USD', 'days': 5, 'nights': 4, 'countries': ['Spain'], 'destination': 'spain',
        'image': 'madrid-plaza-mayor.jpg', 'gallery': [], 'order': 17, 'group_size_max': 12,
        'departs_from': 'Nairobi (flights arranged)', 'visa_support': True,
        'description': 'Madrid for galleries and tapas, with a day trip to the walled city of Toledo.',
        'highlights': ['Four nights in Madrid', 'Toledo day trip', 'Tapas evening'],
        'inclusions': ['4 nights hotel in Madrid', 'Daily breakfast', 'Toledo day trip', 'Schengen visa application support'],
        'exclusions': ['International flights (quoted separately)', 'Visa fees', *INTL_EXCLUSIONS],
        'itinerary': [
            day(1, 'Arrive in Madrid', 'Transfer to the hotel.', [], [], 'Hotel, Madrid'),
            day(2, 'Madrid', 'The Prado and Plaza Mayor.', [], [B], 'Hotel, Madrid'),
            day(3, 'Toledo', 'A day in the walled city.', ['Toledo day trip'], [B], 'Hotel, Madrid'),
            day(4, 'Madrid at leisure', 'A tapas evening.', ['Tapas trail'], [B], 'Hotel, Madrid'),
            day(5, 'Departure', 'Transfer to the airport.', [], [B]),
        ],
    },
]

# Regional groupings for the homepage packages tabs, as specified by the
# business. Independent of the categories above: a tour keeps its one product
# line and can sit in several areas.
AREAS = [
    {'slug': 'kenyan', 'name': 'Kenyan', 'order': 1, 'areas': [
        ('diani', 'Diani'), ('watamu-malindi', 'Watamu/Malindi'), ('maasai-mara', 'Maasai Mara'),
        ('amboseli', 'Amboseli'), ('tsavo', 'Tsavo'),
    ]},
    {'slug': 'europe', 'name': 'Europe', 'order': 2, 'areas': [
        ('germany', 'Germany'), ('spain', 'Spain'), ('france', 'France'), ('italy', 'Italy'),
    ]},
    {'slug': 'africa', 'name': 'Africa', 'order': 3, 'areas': [
        ('south-africa', 'South Africa'), ('egypt', 'Egypt'), ('zanzibar', 'Zanzibar'), ('mauritius', 'Mauritius'),
    ]},
    {'slug': 'asia-middle-east', 'name': 'Asia & Middle East', 'order': 4, 'areas': [
        ('thailand', 'Thailand'), ('malaysia', 'Malaysia'), ('singapore', 'Singapore'), ('dubai', 'Dubai'),
    ]},
]

# What the homepage's "Where we go" portrait cards show for the Kenyan areas:
# tag, teaser, card image, and the Kenya destination places each covers (by
# name). Teasers restate the place blurbs above.
AREA_DETAILS = {
    'diani': {'tag': 'Locals / Kenya', 'image': 'diani-beach-palms.jpg', 'places': ['Diani Beach'],
              'description': 'White sand south of Mombasa, with reef snorkelling and dhow cruises.'},
    'watamu-malindi': {'tag': 'Locals / Kenya', 'image': 'kenya-coast-sunset.jpg', 'places': ['Watamu & Malindi'],
                       'description': 'Marine-park snorkelling at Watamu and the Swahili old town of Malindi.'},
    'maasai-mara': {'tag': 'Locals / Kenya', 'image': 'mara-wildebeest-migration.jpg', 'places': ['Maasai Mara'],
                    'description': 'Big cats year-round, and the river crossings of the migration from July.'},
    'amboseli': {'tag': 'Locals / Kenya', 'image': 'amboseli-elephant-kilimanjaro.jpg', 'places': ['Amboseli'],
                 'description': 'Elephant herds with Kilimanjaro rising behind them on clear mornings.'},
    'tsavo': {'tag': 'Locals / Kenya', 'image': 'tsavo-red-elephants.jpg', 'places': ['Tsavo East & West'],
              'description': 'Red-dust elephants and the Mzima Springs hippo pools in Kenya’s largest park.'},
}

# Existing tours placed in the areas they actually visit (by title). Areas with
# no tour yet stay empty rather than being filled with invented packages.
AREA_TOURS = {
    'diani': ['Diani Beach Escape'],
    'maasai-mara': [
        'Maasai Mara, 3 Days', 'Mara Balloon Safari Weekend', 'Mara–Serengeti Migration',
        'East Africa Grand Safari', 'Safari & Zanzibar Beach',
    ],
    'amboseli': ['Amboseli & Kilimanjaro Views'],
    'tsavo': ['Tsavo East & West'],
    'france': ['Paris City Break', 'Grand European Tour'],
    'italy': ['Rome, Florence & Venice', 'Florence & Tuscany Short Break', 'Grand European Tour'],
    'spain': ['Barcelona & Madrid', 'Madrid & Toledo City Break'],
    'zanzibar': ['Safari & Zanzibar Beach'],
}
