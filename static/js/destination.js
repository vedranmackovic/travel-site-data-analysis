
  // 1. Destination data
  const destinations = {
    Canyon: {
      name: "Grand Canyon",
      description: `A sheer mile-deep gorge carved over six million years by
       the Colorado River, offering vistas that shift from rust-red cliffs to shadowed side canyons.
       Visitors can stroll along the South Rim's scenic trails, ride mule trips down to the river, 
       float rapids, or soar by helicopter above the vast canyon. It's one of Earth's 
       greatest geological spectacles and a UNESCO World Heritage site, with over 4.7 million visitors yearly.`,
      images: ["Canyon1.jpg", "Canyon2.jpg", "Canyon3.jpg"]
    },
    Niagara:{
        name: "Niagara Falls",
        description: `A spectacular triad of waterfalls straddling the US-Canada border, Niagara Falls is famed 
        for its thunderous Horseshoe Falls, scenic walking paths, and mist-drenched cliffside view decks. 
        Activities include the Maid of the Mist boat, Cave of the Winds walkways, trolley tours, and the lush 
        Queen Victoria Park on the Canadian side . A honeymoon favorite for centuries, it blends raw natural 
        power with charming urban tourism around 400 acres of parkland .`,
        images: ["Niagara1.jpg", "Niagara2.jpg", "Niagara3.jpg"]
    },
    Banff:{
        name: "Banff National Park",
        description: `Canada's first national park, nestled in the heart of the Rockies, captivates with towering glaciated peaks, 
        turquoise lakes, and dense forests. Watch wildlife (bears, elk, wolves), paddle Lake Louise or Moraine Lake, 
        drive the Icefields Parkway, ride gondolas, ski or hike alpine trails—year-round adventure awaits. 
        With over 2,500 square miles and a town framed by Cascade Mountain, Banff blends wilderness and charm like nowhere else.`,
        images: ["Banff1.jpg", "Banff2.jpg", "Banff3.jpg"]
    },
    NewYork:{
        name: "New York City",
        description: `The city that never sleeps, New York dazzles with a skyline of legendary landmarks — 
        from the Empire State Building and Central Park to the Statue of Liberty and Times Square. 
        It's a cultural powerhouse with world-class museums like the MET and MoMA, a Broadway theatre district, 
        and neighborhoods bursting with diversity and energy. Whether you're strolling through SoHo, 
        catching a show, or watching the city lights from the Brooklyn Bridge, NYC pulses with life day and night.`,
        images: ["NewYork1.jpg", "NewYork2.jpg", "NewYork3.jpg"]
    },
    Hawaii:{
        name: "Hawai'i Islands",
        description: `Hawaii is a Pacific paradise of volcanic landscapes, lush rainforests, waterfalls, 
        and palm-lined beaches. Each island offers something distinct: O'ahu's surf and nightlife, Maui's 
        Road to Hāna and luxury, Kaua'i's dramatic cliffs, and the Big Island's lava flows and stargazing. 
        Visitors can hike volcanoes, snorkel with sea turtles, attend a traditional luau, or simply relax on 
        golden sands surrounded by aloha spirit.`,
        images: ["Hawaii1.jpg","Hawaii2.jpg","Hawaii3.jpg"]
    },
    MachuPicchu:{
        name: "Machu Picchu",
        description: `A mystical Incan citadel nestled high in the Andes, Machu Picchu is a marvel of ancient 
        engineering and sacred design. Shrouded in clouds and mystery, it offers breathtaking views, 
        intricate stonework, and rich cultural significance. Whether you arrive by train or trek the Inca Trail, 
        the experience of standing atop its terraces, with llamas grazing nearby, is unforgettable.`,
        images: ["MachuPicchu1.jpg","MachuPicchu2.jpg","MachuPicchu3.jpg"]
    },
    Rio:{
        name: "Rio de Janeiro",
        description: `Famed for its carnival spirit, dramatic landscapes, and samba rhythms, Rio is a city of vibrant contrasts. 
        Christ the Redeemer watches over lush mountains, golden beaches like Copacabana, and a buzzing urban life. 
        Visitors can hike Sugarloaf Mountain, dance in Lapa, or relax by the ocean with a caipirinha in hand — 
        all under the tropical sun.`,
        images: ["Rio1.jpg","Rio2.jpg","Rio3.jpg"]
    },
    Patagonia:{
        name: "Patagonia - Torres del Paine",
        description: `Patagonia is a vast wilderness at the edge of the world, home to jagged peaks, glaciers, 
        wind-swept steppes, and pristine lakes. From trekking in Torres del Paine to cruising past icebergs in 
        Los Glaciares National Park, it's a dream for adventurers. Wildlife like guanacos, condors, and penguins 
        add to its untamed magic.`,
        images: ["Patagonia1.jpg","Patagonia2.jpg","Patagonia3.jpg"]
    },
    Galapagos:{
        name: "Galápagos Islands",
        description: `A living laboratory of evolution, the Galápagos Islands are teeming with unique wildlife — 
        from giant tortoises to blue-footed boobies. Located 1,000 km off Ecuador's coast, 
        the archipelago invites exploration by boat, snorkeling, and guided hikes. Protected as a UNESCO site, 
        it's a rare opportunity to witness animals and ecosystems that exist nowhere else.`,
        images: ["Galapagos1.jpg","Galapagos2.jpg","Galapagos3.jpg"]
    },
    Paris:{
        name: "Paris",
        description: `The City of Light enchants with its timeless elegance, romantic streets, 
        and world-renowned art and fashion. Stroll along the Seine, climb the Eiffel Tower, 
        explore the Louvre, and sip espresso at a sidewalk café. Paris blends old-world charm with modern flair, 
        offering unforgettable experiences in every arrondissement.`,
        images: ["Paris1.jpg","Paris2.jpg","Paris3.jpg"]
    },
    Rome:{
        name: "Rome",
        description: `Rome is a living museum where ancient ruins and Renaissance wonders coexist. 
        From the Colosseum and Roman Forum to Vatican City and the Pantheon, history breathes in every cobblestone. 
        Savor pasta in a hidden trattoria, toss a coin in the Trevi Fountain, and soak in la dolce vita.`,
        images: ["Rome1.jpg","Rome2.jpg","Rome3.jpg"]
    },
    Barcelona:{
        name: "Barcelona",
        description: `Barcelona bursts with creativity, color, and coastal charm. The architecture of Antoni Gaudí, 
        especially the Sagrada Família and Park Güell, defines the city's whimsical skyline. Explore Gothic alleys, 
        feast on tapas, and unwind on Mediterranean beaches — all while surrounded by Catalonian culture and flair.`,
        images: ["Barcelona1.jpg","Barcelona2.jpg","Barcelona3.jpg"]
    },
    BlueLagoon:{
        name: "Blue Lagoon",
        description: `A geothermal wonder in a lava field, the Blue Lagoon offers milky-blue waters rich in silica and minerals. 
        Visitors can soak in steamy pools while surrounded by volcanic landscapes and distant snowcaps. 
        With spa treatments, saunas, and the surreal Icelandic light, it's a rejuvenating escape unlike any other.`,
        images: ["BlueLagoon1.jpg","BlueLagoon2.jpg","BlueLagoon3.jpg"]
    },
    Alps:{
        name: "Swiss Alps",
        description: `A panorama of jagged peaks, alpine meadows, and glacial lakes, 
        the Swiss Alps offer four-season adventure. Ski world-class resorts like Zermatt or St. Moritz, 
        hike flower-strewn trails, or ride scenic trains like the Glacier Express. 
        Villages with wooden chalets and cowbells add postcard charm to this pristine region.`,
        images: ["Alps1.jpg","Alps2.jpg","Alps3.jpg"]
    },
    Santorini:{
        name: "Santorini",
        description: `Santorini stuns with its whitewashed buildings, blue domes, and caldera views over the Aegean Sea. 
        Formed by volcanic eruption, it blends dramatic cliffs, sunsets in Oia, black-sand beaches, 
        and local wine tasting. Romance, mythology, and Mediterranean magic converge on this iconic island.`,
        images: ["Santorini1.jpg","Santorini2.jpg","Santorini3.jpg"]
    },
    Fjord:{
        name: "Fjord Norway",
        description: `Norway's fjords are nature's masterpieces — steep cliffs, thundering waterfalls, 
        and glassy inlets carved by ancient glaciers. Cruise through Geirangerfjord or Nærøyfjord, 
        explore charming fishing villages, and hike to panoramic lookouts. With midnight sun or northern lights, 
        every season reveals new beauty.`,
        images: ["Fjord1.jpg","Fjord2.jpg","Fjord3.jpg"]
    },
    Tokyo:{
        name: "Tokyo",
        description: `Tokyo is a dazzling mix of ultra-modern innovation and centuries-old tradition. 
        Neon-lit skyscrapers stand beside ancient temples like Sensō-ji, while sushi counters and 
        robot cafés compete with tea ceremonies. Ride the Shinkansen, explore Shibuya Crossing, 
        or find peace in a cherry blossom garden — Tokyo is endlessly fascinating.`,
        images: ["Tokyo1.jpg","Tokyo2.jpg","Tokyo3.jpg"]
    },
    Bali:{
        name: "Bali",
        description: `Bali is an island of lush rice terraces, ancient temples, and surfing beaches 
        framed by volcanic peaks. Its spiritual heart beats in Ubud, while beach life thrives in Seminyak or Uluwatu. 
        From yoga retreats to coral reefs, Bali offers a harmonious blend of nature, culture, and wellness.`,
        images: ["Bali1.jpg","Bali2.jpg","Bali3.jpg"]
    },
    GreatWall:{
        name: "Great Wall of China",
        description: `Winding over 13,000 miles across mountains and deserts, the Great Wall of China 
        is one of the most iconic and ambitious feats of human engineering. Built over centuries to protect Chinese empires, 
        it offers breathtaking hikes, watchtowers, and cultural insight. Visiting sections like 
        Mutianyu or Jinshanling combines natural beauty with awe-inspiring history.`,
        images: ["GreatWall1.jpg","GreatWall2.jpg","GreatWall3.jpg"]
    },
    TajMahal:{
        name: "Taj Mahal",
        description: `The Taj Mahal, a marble masterpiece in Agra, stands as a timeless symbol of love and devotion. 
        Commissioned by Emperor Shah Jahan for his late wife Mumtaz Mahal, its ivory domes and intricate 
        inlay work are breathtaking. At sunrise or sunset, the monument glows, reflecting beauty and symmetry 
        unmatched in the world.`,
        images: ["TajMahal1.jpg","TajMahal2.jpg","TajMahal3.jpg"]
    },
    Phuket:{
        name: "Phuket",
        description: `Thailand's largest island, Phuket blends tropical beaches, buzzing nightlife, 
        and rich cultural sites. From Patong's party scene to serene Big Buddha viewpoints and Phang Nga Bay cruises, 
        there's something for everyone. Street food markets, Muay Thai matches, and island-hopping tours make it a 
        vibrant escape in the Andaman Sea.`,
        images: ["Phuket1.jpg","Phuket2.jpg","Phuket3.jpg"]
    },
    Serengeti:{
        name: "Serengeti National Park",
        description: `A vast savannah teeming with life, Serengeti National Park is the stage for the Great Migration — 
        millions of wildebeest and zebras crossing plains and rivers. Home to the “Big Five,” 
        it offers some of Africa's best wildlife viewing. Safari drives at dawn reveal lions hunting, 
        elephants roaming, and landscapes that stretch to the horizon.`,
        images: ["Serengeti1.jpg","Serengeti2.jpg","Serengeti3.jpg"]
    },
    Cape:{
        name: "Cape Town",
        description: `Cape Town is a city of striking contrasts — nestled between Table Mountain and the Atlantic, 
        it offers beaches, vineyards, and rich history. Take a cable car to the summit, visit Robben Island, 
        explore the Cape Winelands, or enjoy the colorful Bo-Kaap district. Its cultural diversity and natural 
        beauty make it one of Africa's most captivating cities.`,
        images: ["Cape1.jpg","Cape2.jpg","Cape3.jpg"]
    },
    Victoria:{
        name: "Victoria Falls",
        description: `Known as "The Smoke That Thunders," Victoria Falls is one of the largest and most powerful 
        waterfalls in the world. The Zambezi River plunges over 100 meters into a dramatic gorge, sending mist and rainbows 
        into the air. Adventure seekers can bungee, whitewater raft, or swim in the Devil's Pool at the edge of the falls.`,
        images: ["Victoria1.jpg","Victoria2.jpg","Victoria3.jpg"]
    },
    Madagascar:{
        name: "Madagascar",
        description: `Madagascar, the world's fourth-largest island, is a biodiversity hotspot like no other. 
        Home to unique species like lemurs and baobab trees, its landscapes range from rainforests and 
        dry spiny deserts to pristine coral reefs. Ecotourism thrives in its national parks, offering visitors 
        an otherworldly natural experience.`,
        images: ["Madagascar1.jpg","Madagascar2.jpg","Madagascar3.jpg"]
    },
    Giza:{
        name: "Pyramids of Giza",
        description: `Giza is home to the iconic Pyramids and the Great Sphinx, standing as 
        ancient guardians on the edge of the Sahara. These monumental tombs, built over 4,500 years ago, 
        continue to awe with their scale and mystery. Nearby museums and camel rides add context to Egypt's 
        fascinating ancient history.`,
        images: ["Giza1.jpg","Giza2.jpg","Giza3.png"]
    },
    BarrierReef:{
        name: "Great Barrier Reef",
        description: `The world's largest coral reef system, the Great Barrier Reef stretches over 2,300 kilometers 
        along Australia's northeast coast. It hosts an underwater paradise of coral gardens, sea turtles, reef sharks, 
        and vibrant fish. Snorkeling, scuba diving, or flying over it by seaplane reveals one of Earth's 
        most breathtaking natural wonders.`,
        images: ["BarrierReef1.jpg","BarrierReef2.jpg","BarrierReef3.jpg"]
    },
    Sydney:{
        name: "Sydney Opera House",
        description: `Sydney dazzles with its iconic harbor, the white sails of the Opera House, 
        and the arching Harbour Bridge. Bondi Beach, Darling Harbour, and historic The Rocks all offer coastal charm, 
        while the Blue Mountains lie just beyond. Culture, nature, and cosmopolitan flair unite in this dynamic Australian city.`,
        images: ["Sydney1.jpg","Sydney2.jpg","Sydney3.jpg"]  
    },
    Uluru:{
        name: "Uluru (Ayers Rock)",
        description: `Uluru, also known as Ayers Rock, is a sacred sandstone monolith rising from Australia's Red Centre. 
        Its color changes with the light, especially stunning at sunrise and sunset. Deeply significant to 
        the Anangu people, it offers guided walks, Aboriginal stories, and a profound connection to the land.`,
        images: ["Uluru1.jpg","Uluru2.jpg","Uluru3.jpg"]
    },
    Antartica:{
        name: "Antarctic Peninsula",
        description: `A journey to the Antarctic Peninsula is a true expedition to Earth's last great wilderness. 
        Towering icebergs, glaciers, and snow-covered mountains frame colonies of penguins, seals, and passing whales. 
        Visitors arrive by icebreaker or cruise, stepping onto a continent untouched by cities and rich with raw, frozen beauty.`,
        images: ["Antartica1.jpg","Antartica2.jpg","Antartica3.jpg"]
    }
  };

  const params = new URLSearchParams(window.location.search);
  const place = params.get("place");

  if (place && destinations[place]) {
    const destination = destinations[place];
    document.getElementById("location-name").textContent = destination.name.toUpperCase();
    document.getElementById("location-description").textContent = destination.description;
    document.getElementById("img1").src = `../static/img/${destination.images[0]}`;
    document.getElementById("img2").src = `../static/img/${destination.images[1]}`;
    document.getElementById("img3").src = `../static/img/${destination.images[2]}`;
  } else {
    document.getElementById("location-name").textContent = "DESTINATION NOT FOUND";
    document.getElementById("location-description").textContent = "We couldn't load the destination info.";
  }
