from models import db, Destination, Accommodation, Transport

def create_destinations():
    if Destination.query.first():
        print("Destinations already filled.")
        return

    destinations = [
        {
            "name": "Grand Canyon",
            "continent": "North America",
            "place": "Arizona, USA",
            "short_desc": """One of the most iconic natural landmarks in the world, 
                the Grand Canyon offers unforgettable views, hiking trails, and sunset experiences that leave visitors in awe.""",
            "long_desc": """A sheer mile-deep gorge carved over six million years by
                the Colorado River, offering vistas that shift from rust-red cliffs to shadowed side canyons.
                Visitors can stroll along the South Rim's scenic trails, ride mule trips down to the river, 
                float rapids, or soar by helicopter above the vast canyon. It's one of Earth's 
                greatest geological spectacles and a UNESCO World Heritage site, with over 4.7 million visitors yearly.""",
            "image1": "Canyon1.jpg",
            "image2": "Canyon2.jpg",
            "image3": "Canyon3.jpg",
            "service_price": 120,
            "accommodation": {
                "Hotel": 140,
                "Hostel": 55,
                "Airbnb": 95,
                "Villa": 210,
                "Resort": 250
            },
            "transport": {
                "Bus": 280,
                "Train": 250,
                "Plane": 450,
                "Car rental": 370
            }
        },
        {
            "name": "Niagara Falls",
            "continent": "North America",
            "place": "Ontario, Canada",
            "short_desc": """One of the most powerful and awe-inspiring waterfalls in the world.
                 Popular for its boat tours and cross-border views.""",
            "long_desc": """A spectacular triad of waterfalls straddling the US-Canada border, Niagara Falls is famed 
                for its thunderous Horseshoe Falls, scenic walking paths, and mist-drenched cliffside view decks. 
                Activities include the Maid of the Mist boat, Cave of the Winds walkways, trolley tours, and the lush 
                Queen Victoria Park on the Canadian side . A honeymoon favorite for centuries, it blends raw natural 
                power with charming urban tourism around 400 acres of parkland .""",
            "image1": "Niagara1.jpg",
            "image2": "Niagara2.jpg",
            "image3": "Niagara3.jpg",
            "service_price": 140,
            "accommodation": {
                "Hotel": 160,
                "Hostel": 60,
                "Airbnb": 100,
                "Villa": 230,
                "Resort": 270
            },
            "transport": {
                "Bus": 290,
                "Train": 270,
                "Plane": 480,
                "Car rental": 370
            }
        },
        {
            "name": "Banff National Park",
            "continent": "North America",
            "place": "Alberta, Canada",
            "short_desc": """A jewel of the Canadian Rockies with turquoise lakes, 
                alpine trails, and scenic beauty. Ideal for nature and adventure lovers.""",
            "long_desc": """Canada's first national park, nestled in the heart of the Rockies, captivates with towering glaciated peaks, 
                turquoise lakes, and dense forests. Watch wildlife (bears, elk, wolves), paddle Lake Louise or Moraine Lake, 
                drive the Icefields Parkway, ride gondolas, ski or hike alpine trails—year-round adventure awaits. 
                With over 2,500 square miles and a town framed by Cascade Mountain, Banff blends wilderness and charm like nowhere else.""",
            "image1": "Banff1.jpg",
            "image2": "Banff2.jpg",
            "image3": "Banff3.jpg",
            "service_price": 160,
            "accommodation": {
                "Hotel": 180,
                "Hostel": 65,
                "Airbnb": 110,
                "Villa": 240,
                "Resort": 290
            },
            "transport": {
                "Bus": 310,
                "Train": 330,
                "Plane": 520,
                "Car rental": 390
            }
        },
        {
            "name": "New York",
            "continent": "North America",
            "place": "New York, USA",
            "short_desc": """A global icon of culture, entertainment, and energy. See Broadway, 
                explore museums, or just roam the city streets.""",
            "long_desc": """The city that never sleeps, New York dazzles with a skyline of legendary landmarks — 
                from the Empire State Building and Central Park to the Statue of Liberty and Times Square. 
                It's a cultural powerhouse with world-class museums like the MET and MoMA, a Broadway theatre district, 
                and neighborhoods bursting with diversity and energy. Whether you're strolling through SoHo, 
                catching a show, or watching the city lights from the Brooklyn Bridge, NYC pulses with life day and night.""",
            "image1": "NewYork1.jpg",
            "image2": "NewYork2.jpg",
            "image3": "NewYork3.jpg",
            "service_price": 100,
            "accommodation": {
                "Hotel": 220,
                "Hostel": 75,
                "Airbnb": 150,
                "Villa": 310,
                "Resort": 350
            },
            "transport": {
                "Bus": 300,
                "Train": 320,
                "Plane": 480,
                "Car rental": 390
            }
        },
        {
            "name": "Hawaii Islands",
            "continent": "North America",
            "place": "Hawai'i, USA",
            "short_desc": """Known for their volcanic landscapes, tropical beaches, and rich Polynesian culture,
                 the Hawaiian Islands are a dream destination for both relaxation and adventure.""",
            "long_desc": """Hawaii is a Pacific paradise of volcanic landscapes, lush rainforests, waterfalls, 
                and palm-lined beaches. Each island offers something distinct: O'ahu's surf and nightlife, Maui's 
                Road to Hāna and luxury, Kaua'i's dramatic cliffs, and the Big Island's lava flows and stargazing. 
                Visitors can hike volcanoes, snorkel with sea turtles, attend a traditional luau, or simply relax on 
                golden sands surrounded by aloha spirit.""",
            "image1": "Hawaii1.jpg",
            "image2": "Hawaii2.jpg",
            "image3": "Hawaii3.jpg",
            "service_price": 210,
            "accommodation": {
                "Hotel": 210,
                "Hostel": 70,
                "Airbnb": 140,
                "Villa": 300,
                "Resort": 340
            },
            "transport": {
                "Bus": 460,
                "Train": 480,
                "Plane": 750,
                "Car rental": 500
            }
        },
        {
            "name": "Machu Picchu",
            "continent": "South America",
            "place": "Andes Mountains, Peru",
            "short_desc": """This ancient Incan citadel nestled high in the clouds is one of the world's most iconic archaeological sites. 
                Hike the Inca Trail or ride the scenic train to discover breathtaking views and rich history.""",
            "long_desc": """A mystical Incan citadel nestled high in the Andes, Machu Picchu is a marvel of ancient 
                engineering and sacred design. Shrouded in clouds and mystery, it offers breathtaking views, 
                intricate stonework, and rich cultural significance. Whether you arrive by train or trek the Inca Trail, 
                the experience of standing atop its terraces, with llamas grazing nearby, is unforgettable.""",
            "image1": "MachuPicchu1.jpg",
            "image2": "MachuPicchu2.jpg",
            "image3": "MachuPicchu3.jpg",
            "service_price": 130,
            "accommodation": {
                "Hotel": 120,
                "Hostel": 45,
                "Airbnb": 80,
                "Villa": 190,
                "Resort": 220
            },
            "transport": {
                "Bus": 320,
                "Train": 300,
                "Plane": 520,
                "Car rental": 410
            }
        },
        {
            "name": "Rio de Janeiro",
            "continent": "South America",
            "place": "Rio de Janeiro, Brazil",
            "short_desc": """Explore the vibrant rhythm of Rio with its stunning beaches, 
                the towering Christ the Redeemer statue, and colorful street culture. A perfect blend of nature, energy, and beauty.""",
            "long_desc": """Famed for its carnival spirit, dramatic landscapes, and samba rhythms, Rio is a city of vibrant contrasts. 
                Christ the Redeemer watches over lush mountains, golden beaches like Copacabana, and a buzzing urban life. 
                Visitors can hike Sugarloaf Mountain, dance in Lapa, or relax by the ocean with a caipirinha in hand — 
                all under the tropical sun.""",
            "image1": "Rio1.jpg",
            "image2": "Rio2.jpg",
            "image3": "Rio3.jpg",
            "service_price": 120,
            "accommodation": {
                "Hotel": 150,
                "Hostel": 55,
                "Airbnb": 90,
                "Villa": 200,
                "Resort": 240
            },
            "transport": {
                "Bus": 400,
                "Train": 420,
                "Plane": 690,
                "Car rental": 470
            }
        },
        {
            "name": "Patagonia",
            "continent": "South America",
            "place": "Chile & Argentina",
            "short_desc": """A haven for nature lovers and trekkers, Patagonia offers jagged peaks, 
                glacial lakes, and wildlife-filled trails. The Torres del Paine National Park is a bucket-list adventure.""",
            "long_desc": """Patagonia is a vast wilderness at the edge of the world, home to jagged peaks, glaciers, 
                wind-swept steppes, and pristine lakes. From trekking in Torres del Paine to cruising past icebergs in 
                Los Glaciares National Park, it's a dream for adventurers. Wildlife like guanacos, condors, and penguins 
                add to its untamed magic.""",
            "image1": "Patagonia1.jpg",
            "image2": "Patagonia2.jpg",
            "image3": "Patagonia3.jpg",
            "service_price": 150,
            "accommodation": {
                "Hotel": 130,
                "Hostel": 50,
                "Airbnb": 85,
                "Villa": 195,
                "Resort": 230
            },
            "transport": {
                "Bus": 380,
                "Train": 360,
                "Plane": 630,
                "Car rental": 480
            }
        },
        {
            "name": "Galapagos",
            "continent": "South America",
            "place": "Ecuador",
            "short_desc": """Walk among giant tortoises, snorkel with sea lions, 
                and experience ecosystems found nowhere else on Earth. The Galápagos offer a one-of-a-kind wildlife encounter.""",
            "long_desc": """A living laboratory of evolution, the Galápagos Islands are teeming with unique wildlife — 
                from giant tortoises to blue-footed boobies. Located 1,000 km off Ecuador's coast, 
                the archipelago invites exploration by boat, snorkeling, and guided hikes. Protected as a UNESCO site, 
                it's a rare opportunity to witness animals and ecosystems that exist nowhere else.""",
            "image1": "Galapagos1.jpg",
            "image2": "Galapagos2.jpg",
            "image3": "Galapagos3.jpg",
            "service_price": 180,
            "accommodation": {
                "Hotel": 200,
                "Hostel": 80,
                "Airbnb": 120,
                "Villa": 260,
                "Resort": 320
            },
            "transport": {
                "Bus": 390,
                "Train": 370,
                "Plane": 620,
                "Car rental": 450
            }
        },
        {
            "name": "Paris",
            "continent": "Europe",
            "place": "Paris, France",
            "short_desc": """The City of Light is famous for iconic landmarks like the Eiffel Tower, 
                world-class museums, and charming streets along the Seine River.""",
            "long_desc": """The City of Light enchants with its timeless elegance, romantic streets, 
                and world-renowned art and fashion. Stroll along the Seine, climb the Eiffel Tower, 
                explore the Louvre, and sip espresso at a sidewalk café. Paris blends old-world charm with modern flair, 
                offering unforgettable experiences in every arrondissement.""",
            "image1": "Paris1.jpg",
            "image2": "Paris2.jpg",
            "image3": "Paris3.jpg",
            "service_price": 120,
            "accommodation": {
                "Hotel": 210,
                "Hostel": 70,
                "Airbnb": 135,
                "Villa": 290,
                "Resort": 330
            },
            "transport": {
                "Bus": 90,
                "Train": 70,
                "Plane": 120,
                "Car rental": 160
            }
        },
        {
            "name": "Rome",
            "continent": "Europe",
            "place": "Rome, Italy",
            "short_desc": """Known for ancient ruins like the Colosseum and Vatican City, 
                Rome combines rich history with vibrant street life and delicious cuisine.""",
            "long_desc": """Rome is a living museum where ancient ruins and Renaissance wonders coexist. 
                From the Colosseum and Roman Forum to Vatican City and the Pantheon, history breathes in every cobblestone. 
                Savor pasta in a hidden trattoria, toss a coin in the Trevi Fountain, and soak in la dolce vita.""",
            "image1": "Rome1.jpg",
            "image2": "Rome2.jpg",
            "image3": "Rome3.jpg",
            "service_price": 100,
            "accommodation": {
                "Hotel": 200,
                "Hostel": 65,
                "Airbnb": 125,
                "Villa": 275,
                "Resort": 320
            },
            "transport": {
                "Bus": 100,
                "Train": 85,
                "Plane": 150,
                "Car rental": 170
            }
        },
        {
            "name": "Barcelona",
            "continent": "Europe",
            "place": "Barcelona, Spain",
            "short_desc": """Known for Gaudí's colorful architecture, Mediterranean beaches,
                 and lively nightlife, Barcelona is a cultural hotspot.""",
            "long_desc": """Barcelona bursts with creativity, color, and coastal charm. The architecture of Antoni Gaudí, 
                especially the Sagrada Família and Park Güell, defines the city's whimsical skyline. Explore Gothic alleys, 
                feast on tapas, and unwind on Mediterranean beaches — all while surrounded by Catalonian culture and flair.""",
            "image1": "Barcelona1.jpg",
            "image2": "Barcelona2.jpg",
            "image3": "Barcelona3.jpg",
            "service_price": 110,
            "accommodation": {
                "Hotel": 190,
                "Hostel": 60,
                "Airbnb": 120,
                "Villa": 260,
                "Resort": 310
            },
            "transport": {
                "Bus": 80,
                "Train": 65,
                "Plane": 110,
                "Car rental": 140
            }
        },
        {
            "name": "Blue Lagoon",
            "continent": "Europe",
            "place": "Iceland",
            "short_desc": """A unique geothermal spa surrounded by volcanic landscapes,
                 offering relaxing warm waters in a stunning natural setting.""",
            "long_desc": """A geothermal wonder in a lava field, the Blue Lagoon offers milky-blue waters rich in silica and minerals. 
                Visitors can soak in steamy pools while surrounded by volcanic landscapes and distant snowcaps. 
                With spa treatments, saunas, and the surreal Icelandic light, it's a rejuvenating escape unlike any other.""",
            "image1": "BlueLagoon1.jpg",
            "image2": "BlueLagoon2.jpg",
            "image3": "BlueLagoon3.jpg",
            "service_price": 150,
            "accommodation": {
                "Hotel": 240,
                "Hostel": 90,
                "Airbnb": 150,
                "Villa": 320,
                "Resort": 370
            },
            "transport": {
                "Bus": 170,
                "Train": 160,
                "Plane": 280,
                "Car rental": 200
            }
        },
        {
            "name": "Swiss Alps",
            "continent": "Europe",
            "place": "Switzerland",
            "short_desc": """Famous for breathtaking mountain views, hiking, and ski resorts,
                 the Swiss Alps are a haven for nature and adventure lovers.""",
            "long_desc": """A panorama of jagged peaks, alpine meadows, and glacial lakes, 
                the Swiss Alps offer four-season adventure. Ski world-class resorts like Zermatt or St. Moritz, 
                hike flower-strewn trails, or ride scenic trains like the Glacier Express. 
                Villages with wooden chalets and cowbells add postcard charm to this pristine region.""",
            "image1": "Alps1.jpg",
            "image2": "Alps2.jpg",
            "image3": "Alps3.jpg",
            "service_price": 170,
            "accommodation": {
                "Hotel": 230,
                "Hostel": 85,
                "Airbnb": 145,
                "Villa": 310,
                "Resort": 360
            },
            "transport": {
                "Bus": 95,
                "Train": 80,
                "Plane": 130,
                "Car rental": 160
            }
        },
        {
            "name": "Santorini",
            "continent": "Europe",
            "place": "Greece",
            "short_desc": """This beautiful island features whitewashed buildings, 
                crystal-clear waters, and spectacular sunsets over the Aegean Sea.""",
            "long_desc": """Santorini stuns with its whitewashed buildings, blue domes, and caldera views over the Aegean Sea. 
                Formed by volcanic eruption, it blends dramatic cliffs, sunsets in Oia, black-sand beaches, 
                and local wine tasting. Romance, mythology, and Mediterranean magic converge on this iconic island.""",
            "image1": "Santorini1.jpg",
            "image2": "Santorini2.jpg",
            "image3": "Santorini3.jpg",
            "service_price": 130,
            "accommodation": {
                "Hotel": 190,
                "Hostel": 70,
                "Airbnb": 130,
                "Villa": 300,
                "Resort": 340
            },
            "transport": {
                "Bus": 130,
                "Train": 110,
                "Plane": 220,
                "Car rental": 180
            }
        },
        {
            "name": "Fjord",
            "continent": "Europe",
            "place": "Norway",
            "short_desc": """Dramatic fjords with towering cliffs and waterfalls
                 make this a breathtaking destination for cruising and nature exploration.""",
            "long_desc": """Norway's fjords are nature's masterpieces — steep cliffs, thundering waterfalls, 
                and glassy inlets carved by ancient glaciers. Cruise through Geirangerfjord or Nærøyfjord, 
                explore charming fishing villages, and hike to panoramic lookouts. With midnight sun or northern lights, 
                every season reveals new beauty.""",
            "image1": "Fjord1.jpg",
            "image2": "Fjord2.jpg",
            "image3": "Fjord3.jpg",
            "service_price": 160,
            "accommodation": {
                "Hotel": 210,
                "Hostel": 80,
                "Airbnb": 140,
                "Villa": 290,
                "Resort": 350
            },
            "transport": {
                "Bus": 150,
                "Train": 130,
                "Plane": 240,
                "Car rental": 190
            }
        },
        {
            "name": "Tokyo",
            "continent": "Asia",
            "place": "Japan",
            "short_desc": """A vibrant metropolis blending ultra-modern skyscrapers
                 with historic temples, renowned for its food scene and pop culture.""",
            "long_desc": """Tokyo is a dazzling mix of ultra-modern innovation and centuries-old tradition. 
                Neon-lit skyscrapers stand beside ancient temples like Sensō-ji, while sushi counters and 
                robot cafés compete with tea ceremonies. Ride the Shinkansen, explore Shibuya Crossing, 
                or find peace in a cherry blossom garden — Tokyo is endlessly fascinating.""",
            "image1": "Tokyo1.jpg",
            "image2": "Tokyo2.jpg",
            "image3": "Tokyo3.jpg",
            "service_price": 140,
            "accommodation": {
                "Hotel": 220,
                "Hostel": 60,
                "Airbnb": 140,
                "Villa": 310,
                "Resort": 360
            },
            "transport": {
                "Bus": 420,
                "Train": 440,
                "Plane": 700,
                "Car rental": 470
            }
        },
        {
            "name": "Bali",
            "continent": "Asia",
            "place": "Indonesia",
            "short_desc": """Famous for its lush rice terraces, stunning beaches, 
                and spiritual temples, Bali is a tropical paradise for relaxation and adventure.""",
            "long_desc": """Bali is an island of lush rice terraces, ancient temples, and surfing beaches 
                framed by volcanic peaks. Its spiritual heart beats in Ubud, while beach life thrives in Seminyak or Uluwatu. 
                From yoga retreats to coral reefs, Bali offers a harmonious blend of nature, culture, and wellness.""",
            "image1": "Bali1.jpg",
            "image2": "Bali2.jpg",
            "image3": "Bali3.jpg",
            "service_price": 110,
            "accommodation": {
                "Hotel": 110,
                "Hostel": 40,
                "Airbnb": 70,
                "Villa": 170,
                "Resort": 200
            },
            "transport": {
                "Bus": 370,
                "Train": 390,
                "Plane": 650,
                "Car rental": 410
            }
        },
        {
            "name": "Great Wall of China",
            "continent": "Asia",
            "place": "China",
            "short_desc": """One of the world's most iconic landmarks, this ancient wall stretches thousands of miles
                                 offering incredible views and historical significance.""",
            "long_desc": """Winding over 13,000 miles across mountains and deserts, the Great Wall of China 
                is one of the most iconic and ambitious feats of human engineering. Built over centuries to protect Chinese empires, 
                it offers breathtaking hikes, watchtowers, and cultural insight. Visiting sections like 
                Mutianyu or Jinshanling combines natural beauty with awe-inspiring history.""",
            "image1": "GreatWall1.jpg",
            "image2": "GreatWall2.jpg",
            "image3": "GreatWall3.jpg",
            "service_price": 130,
            "accommodation": {
                "Hotel": 160,
                "Hostel": 50,
                "Airbnb": 90,
                "Villa": 200,
                "Resort": 240
            },
            "transport": {
                "Bus": 350,
                "Train": 370,
                "Plane": 600,
                "Car rental": 430
            }
        },
        {
            "name": "Taj Mahal",
            "continent": "Asia",
            "place": "India",
            "short_desc": """The stunning white marble mausoleum is a symbol of love
                 and a UNESCO World Heritage Site attracting millions of visitors annually.""",
            "long_desc": """The Taj Mahal, a marble masterpiece in Agra, stands as a timeless symbol of love and devotion. 
                Commissioned by Emperor Shah Jahan for his late wife Mumtaz Mahal, its ivory domes and intricate 
                inlay work are breathtaking. At sunrise or sunset, the monument glows, reflecting beauty and symmetry 
                unmatched in the world.""",
            "image1": "TajMahal1.jpg",
            "image2": "TajMahal2.jpg",
            "image3": "TajMahal3.jpg",
            "service_price": 120,
            "accommodation": {
                "Hotel": 130,
                "Hostel": 35,
                "Airbnb": 75,
                "Villa": 190,
                "Resort": 210
            },
            "transport": {
                "Bus": 260,
                "Train": 240,
                "Plane": 410,
                "Car rental": 330
            }
        },
        {
            "name": "Phuket",
            "continent": "Asia",
            "place": "Thailand",
            "short_desc": """Known for beautiful beaches, vibrant nightlife, and excellent diving spots,
                 Phuket is a popular island destination for all types of travelers.""",
            "long_desc": """Thailand's largest island, Phuket blends tropical beaches, buzzing nightlife, 
                and rich cultural sites. From Patong's party scene to serene Big Buddha viewpoints and Phang Nga Bay cruises, 
                there's something for everyone. Street food markets, Muay Thai matches, and island-hopping tours make it a 
                vibrant escape in the Andaman Sea.""",
            "image1": "Phuket1.jpg",
            "image2": "Phuket2.jpg",
            "image3": "Phuket3.jpg",
            "service_price": 115,
            "accommodation": {
                "Hotel": 100,
                "Hostel": 30,
                "Airbnb": 60,
                "Villa": 150,
                "Resort": 180
            },
            "transport": {
                "Bus": 360,
                "Train": 340,
                "Plane": 590,
                "Car rental": 440
            }
        },
        {
            "name": "Serengeti National Park",
            "continent": "Africa",
            "place": "Tanzania",
            "short_desc": """Famous for its annual wildebeest migration and abundant wildlife,
                 the Serengeti is a must-see for safari lovers.""",
            "long_desc": """A vast savannah teeming with life, Serengeti National Park is the stage for the Great Migration — 
                millions of wildebeest and zebras crossing plains and rivers. Home to the “Big Five,” 
                it offers some of Africa's best wildlife viewing. Safari drives at dawn reveal lions hunting, 
                elephants roaming, and landscapes that stretch to the horizon.""",
            "image1": "Serengeti1.jpg",
            "image2": "Serengeti2.jpg",
            "image3": "Serengeti3.jpg",
            "service_price": 150,
            "accommodation": {
                "Hotel": 180,
                "Hostel": 50,
                "Airbnb": 100,
                "Villa": 230,
                "Resort": 280
            },
            "transport": {
                "Bus": 370,
                "Train": 350,
                "Plane": 620,
                "Car rental": 460
            }
        },
        {
            "name": "Cape Town",
            "continent": "Africa",
            "place": "South Africa",
            "short_desc": """A vibrant city known for Table Mountain,
                 beautiful beaches, and rich cultural diversity.""",
            "long_desc": """Cape Town is a city of striking contrasts — nestled between Table Mountain and the Atlantic, 
                it offers beaches, vineyards, and rich history. Take a cable car to the summit, visit Robben Island, 
                explore the Cape Winelands, or enjoy the colorful Bo-Kaap district. Its cultural diversity and natural 
                beauty make it one of Africa's most captivating cities.""",
            "image1": "Cape1.jpg",
            "image2": "Cape2.jpg",
            "image3": "Cape3.jpg",
            "service_price": 130,
            "accommodation": {
                "Hotel": 160,
                "Hostel": 55,
                "Airbnb": 90,
                "Villa": 210,
                "Resort": 250
            },
            "transport": {
                "Bus": 410,
                "Train": 430,
                "Plane": 720,
                "Car rental": 490
            }
        },
        {
            "name": "Victoria Falls",
            "continent": "Africa",
            "place": "Zambia/Zimbabwe",
            "short_desc": """One of the largest and most spectacular waterfalls in the world,
                 offering breathtaking views and adventure activities.""",
            "long_desc": """Known as "The Smoke That Thunders," Victoria Falls is one of the largest and most powerful 
                waterfalls in the world. The Zambezi River plunges over 100 meters into a dramatic gorge, sending mist and rainbows 
                into the air. Adventure seekers can bungee, whitewater raft, or swim in the Devil's Pool at the edge of the falls.""",
            "image1": "Victoria1.jpg",
            "image2": "Victoria2.jpg",
            "image3": "Victoria3.jpg",
            "service_price": 140,
            "accommodation": {
                "Hotel": 150,
                "Hostel": 50,
                "Airbnb": 85,
                "Villa": 200,
                "Resort": 240
            },
            "transport": {
                "Bus": 350,
                "Train": 330,
                "Plane": 580,
                "Car rental": 440
            }
        },
        {
            "name": "Madagascar",
            "continent": "Africa",
            "place": "Madagascar",
            "short_desc": """Renowned for its unique wildlife and diverse ecosystems,
                 Madagascar is a paradise for nature and adventure enthusiasts.""",
            "long_desc": """Madagascar, the world's fourth-largest island, is a biodiversity hotspot like no other. 
                Home to unique species like lemurs and baobab trees, its landscapes range from rainforests and 
                dry spiny deserts to pristine coral reefs. Ecotourism thrives in its national parks, offering visitors 
                an otherworldly natural experience.""",
            "image1": "Madagascar1.jpg",
            "image2": "Madagascar2.jpg",
            "image3": "Madagascar3.jpg",
            "service_price": 135,
            "accommodation": {
                "Hotel": 120,
                "Hostel": 45,
                "Airbnb": 80,
                "Villa": 190,
                "Resort": 220
            },
            "transport": {
                "Bus": 330,
                "Train": 310,
                "Plane": 560,
                "Car rental": 420
            }
        },
        {
            "name": "Pyramids of Giza",
            "continent": "Africa",
            "place": "Egypt",
            "short_desc": """The iconic pyramids are one of the Seven Wonders of the Ancient World and a marvel of ancient engineering.
                 Visitors can explore the Great Pyramid, the Sphinx, and learn about Egypt's fascinating history.""",
            "long_desc": """Giza is home to the iconic Pyramids and the Great Sphinx, standing as 
                ancient guardians on the edge of the Sahara. These monumental tombs, built over 4,500 years ago, 
                continue to awe with their scale and mystery. Nearby museums and camel rides add context to Egypt's 
                fascinating ancient history.""",
            "image1": "Giza1.jpg",
            "image2": "Giza2.jpg",
            "image3": "Giza3.png",
            "service_price": 200,
            "accommodation": {
                "Hotel": 140,
                "Hostel": 50,
                "Airbnb": 85,
                "Villa": 200,
                "Resort": 230
            },
            "transport": {
                "Bus": 240,
                "Train": 210,
                "Plane": 380,
                "Car rental": 290
            }
        },
        {
            "name": "Great Barrier Reef",
            "continent": "Australia",
            "place": "Queensland, Australia",
            "short_desc": """The world's largest coral reef system, offering stunning snorkeling,
                 diving, and marine wildlife experiences in crystal-clear waters.""",
            "long_desc": """The world's largest coral reef system, the Great Barrier Reef stretches over 2,300 kilometers 
                along Australia's northeast coast. It hosts an underwater paradise of coral gardens, sea turtles, reef sharks, 
                and vibrant fish. Snorkeling, scuba diving, or flying over it by seaplane reveals one of Earth's 
                most breathtaking natural wonders.""",
            "image1": "BarrierReef1.jpg",
            "image2": "BarrierReef2.jpg",
            "image3": "BarrierReef3.jpg",
            "service_price": 220,
            "accommodation": {
                "Hotel": 220,
                "Hostel": 75,
                "Airbnb": 130,
                "Villa": 300,
                "Resort": 350
            },
            "transport": {
                "Bus": 370,
                "Train": 390,
                "Plane": 640,
                "Car rental": 470
            }
        },
        {
            "name": "Sydney",
            "continent": "Australia",
            "place": "Sydney, Australia",
            "short_desc": """An iconic architectural masterpiece on Sydney Harbour,
                 known for its performing arts shows and breathtaking views.""",
            "long_desc": """Sydney dazzles with its iconic harbor, the white sails of the Opera House, 
                and the arching Harbour Bridge. Bondi Beach, Darling Harbour, and historic The Rocks all offer coastal charm, 
                while the Blue Mountains lie just beyond. Culture, nature, and cosmopolitan flair unite in this dynamic Australian city.""",
            "image1": "Sydney1.jpg",
            "image2": "Sydney2.jpg",
            "image3": "Sydney3.jpg",
            "service_price": 180,
            "accommodation": {
                "Hotel": 210,
                "Hostel": 70,
                "Airbnb": 140,
                "Villa": 290,
                "Resort": 330
            },
            "transport": {
                "Bus": 450,
                "Train": 470,
                "Plane": 740,
                "Car rental": 510
            }
        },
        {
            "name": "Uluru",
            "continent": "Australia",
            "place": "Northern Territory, Australia",
            "short_desc": """A massive sandstone monolith sacred to Indigenous Australians,
                 famous for its dramatic red color at sunrise and sunset.""",
            "long_desc": """Uluru, also known as Ayers Rock, is a sacred sandstone monolith rising from Australia's Red Centre. 
                Its color changes with the light, especially stunning at sunrise and sunset. Deeply significant to 
                the Anangu people, it offers guided walks, Aboriginal stories, and a profound connection to the land.""",
            "image1": "Uluru1.jpg",
            "image2": "Uluru2.jpg",
            "image3": "Uluru3.jpg",
            "service_price": 210,
            "accommodation": {
                "Hotel": 190,
                "Hostel": 65,
                "Airbnb": 110,
                "Villa": 270,
                "Resort": 310
            },
            "transport": {
                "Bus": 430,
                "Train": 410,
                "Plane": 700,
                "Car rental": 490
            }
        },
        {
            "name": "Antartica Peninsula",
            "continent": "Antartica",
            "place": "Antarctica",
            "short_desc": """The most accessible and scenic region of Antarctica, featuring stunning glaciers, 
                abundant wildlife like penguins and seals, and breathtaking icy landscapes. Ideal for expedition cruises 
                and nature adventures.""",
            "long_desc": """A journey to the Antarctic Peninsula is a true expedition to Earth's last great wilderness. 
                Towering icebergs, glaciers, and snow-covered mountains frame colonies of penguins, seals, and passing whales. 
                Visitors arrive by icebreaker or cruise, stepping onto a continent untouched by cities and rich with raw, frozen beauty.""",
            "image1": "Antartica1.jpg",
            "image2": "Antartica2.jpg",
            "image3": "Antartica3.jpg",
            "service_price": 350,
            "accommodation": {
                "Hotel": 300,
                "Hostel": 120,
                "Airbnb": 180,
                "Villa": 400,
                "Resort": 450
            },
            "transport": {
                "Plane": 1300,
            }
        }
    ]

    for data in destinations:
        dest = Destination(
            name=data["name"],
            continent=data["continent"],
            place=data["place"],
            short_description=data["short_desc"],
            long_description=data["long_desc"],
            image1=data["image1"],
            image2=data["image2"],
            image3=data["image3"],
            service_price=data["service_price"]
        )
        db.session.add(dest)
        db.session.flush()

        for acc_type, acc_cost in data["accommodation"].items():
            acc = Accommodation(
                destination_id=dest.id,
                type=acc_type,
                cost=acc_cost
            )
            db.session.add(acc)

        for trans_type, trans_cost in data["transport"].items():
            trans = Transport(
                destination_id=dest.id,
                type=trans_type,
                cost=trans_cost
            )
            db.session.add(trans)

    db.session.commit()
    print("30 destinations added.")