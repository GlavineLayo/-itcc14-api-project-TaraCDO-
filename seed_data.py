"""
Script to populate the database with sample places in Cagayan de Oro City
Run this script after starting MongoDB to populate the database
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["taracdo_db"]
collection = db["establishments"]

# Sample places data for Cagayan de Oro City
places = [
    # MALLS (5 places)
    {
        "name": "SM Downtown Premier",
        "category": "Mall",
        "type": "Mall",
        "description": "A premier shopping mall in downtown Cagayan de Oro with various retail stores, restaurants, and entertainment options.",
        "latitude": 8.4815,
        "longitude": 124.6472,
        "lat": 8.4815,
        "lng": 124.6472,
        "rating": 4.5,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Centrio Mall",
        "category": "Mall",
        "type": "Mall",
        "description": "Modern shopping mall featuring international brands, food court, and cinema.",
        "latitude": 8.4825,
        "longitude": 124.6482,
        "lat": 8.4825,
        "lng": 124.6482,
        "rating": 4.6,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$$"
    },
    {
        "name": "Gaisano Mall",
        "category": "Mall",
        "type": "Mall",
        "description": "Popular shopping destination with department store, supermarket, and various shops.",
        "latitude": 8.4790,
        "longitude": 124.6450,
        "lat": 8.4790,
        "lng": 124.6450,
        "rating": 4.3,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Robinsons Cagayan de Oro",
        "category": "Mall",
        "type": "Mall",
        "description": "Large shopping mall with department store, supermarket, restaurants, and entertainment facilities.",
        "latitude": 8.4750,
        "longitude": 124.6420,
        "lat": 8.4750,
        "lng": 124.6420,
        "rating": 4.4,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Limketkai Mall",
        "category": "Mall",
        "type": "Mall",
        "description": "One of the oldest and most established malls in CDO with diverse shopping and dining options.",
        "latitude": 8.4780,
        "longitude": 124.6440,
        "lat": 8.4780,
        "lng": 124.6440,
        "rating": 4.2,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    
    # RESTAURANTS (6 places)
    {
        "name": "Kagay-anon Restaurant",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Authentic Filipino cuisine specializing in Cagayan de Oro local dishes.",
        "latitude": 8.4830,
        "longitude": 124.6460,
        "lat": 8.4830,
        "lng": 124.6460,
        "rating": 4.5,
        "address": "Divisoria, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Bigby's Cafe & Restaurant",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Popular restaurant chain serving Filipino and international dishes in a cozy atmosphere.",
        "latitude": 8.4810,
        "longitude": 124.6480,
        "lat": 8.4810,
        "lng": 124.6480,
        "rating": 4.4,
        "address": "Centrio Mall, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Missy Bon Bon",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Local favorite restaurant known for its delicious Filipino comfort food and desserts.",
        "latitude": 8.4800,
        "longitude": 124.6455,
        "lat": 8.4800,
        "lng": 124.6455,
        "rating": 4.6,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "Sentro 1850",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Upscale restaurant offering modern Filipino cuisine with a contemporary twist.",
        "latitude": 8.4840,
        "longitude": 124.6470,
        "lat": 8.4840,
        "lng": 124.6470,
        "rating": 4.7,
        "address": "Centrio Mall, Cagayan de Oro City",
        "price_range": "$$$"
    },
    {
        "name": "Cafe Laguna",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Casual dining restaurant serving Filipino dishes, perfect for family gatherings.",
        "latitude": 8.4795,
        "longitude": 124.6465,
        "lat": 8.4795,
        "lng": 124.6465,
        "rating": 4.3,
        "address": "SM Downtown Premier, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Yellow Cab Pizza",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Popular pizza chain offering New York-style pizzas and Italian-American dishes.",
        "latitude": 8.4820,
        "longitude": 124.6475,
        "lat": 8.4820,
        "lng": 124.6475,
        "rating": 4.4,
        "address": "Centrio Mall, Cagayan de Oro City",
        "price_range": "$$"
    },
    
    # LANDMARKS (5 places)
    {
        "name": "Divisoria",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Historic public square and commercial center of Cagayan de Oro, a popular gathering place.",
        "latitude": 8.4835,
        "longitude": 124.6465,
        "lat": 8.4835,
        "lng": 124.6465,
        "rating": 4.5,
        "address": "Divisoria, Cagayan de Oro City",
        "price_range": "Free"
    },
    {
        "name": "St. Augustine Cathedral",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Historic Roman Catholic cathedral, one of the oldest churches in Cagayan de Oro.",
        "latitude": 8.4845,
        "longitude": 124.6455,
        "lat": 8.4845,
        "lng": 124.6455,
        "rating": 4.6,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "Free"
    },
    {
        "name": "Xavier University",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Prestigious Jesuit university, one of the top educational institutions in Mindanao.",
        "latitude": 8.4850,
        "longitude": 124.6480,
        "lat": 8.4850,
        "lng": 124.6480,
        "rating": 4.7,
        "address": "Corrales Avenue, Cagayan de Oro City",
        "price_range": "Free"
    },
    {
        "name": "Cagayan de Oro City Hall",
        "category": "Landmark",
        "type": "Landmark",
        "description": "The seat of local government of Cagayan de Oro City.",
        "latitude": 8.4840,
        "longitude": 124.6475,
        "lat": 8.4840,
        "lng": 124.6475,
        "rating": 4.3,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "Free"
    },
    {
        "name": "Museo de Oro",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Museum showcasing the history, culture, and artifacts of Northern Mindanao.",
        "latitude": 8.4855,
        "longitude": 124.6485,
        "lat": 8.4855,
        "lng": 124.6485,
        "rating": 4.5,
        "address": "Xavier University, Cagayan de Oro City",
        "price_range": "$"
    },
    
    # DORMS/HOTELS (5 places)
    {
        "name": "Seda Centrio",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Modern hotel located in Centrio Mall area, offering comfortable accommodations.",
        "latitude": 8.4828,
        "longitude": 124.6485,
        "lat": 8.4828,
        "lng": 124.6485,
        "rating": 4.6,
        "address": "Centrio Mall, Cagayan de Oro City",
        "price_range": "$$$"
    },
    {
        "name": "Limketkai Luxe Hotel",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Boutique hotel offering elegant rooms and excellent service in the heart of CDO.",
        "latitude": 8.4785,
        "longitude": 124.6445,
        "lat": 8.4785,
        "lng": 124.6445,
        "rating": 4.5,
        "address": "Limketkai Mall, Cagayan de Oro City",
        "price_range": "$$$"
    },
    {
        "name": "Red Planet Cagayan de Oro",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Budget-friendly hotel chain offering clean and comfortable rooms.",
        "latitude": 8.4815,
        "longitude": 124.6470,
        "lat": 8.4815,
        "lng": 124.6470,
        "rating": 4.2,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "CDO Student Dormitory",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Affordable student dormitory near universities, perfect for students and budget travelers.",
        "latitude": 8.4860,
        "longitude": 124.6480,
        "lat": 8.4860,
        "lng": 124.6480,
        "rating": 4.0,
        "address": "Near Xavier University, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "Grand Caprice Hotel",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Well-established hotel in downtown CDO with restaurant and event facilities.",
        "latitude": 8.4832,
        "longitude": 124.6468,
        "lat": 8.4832,
        "lng": 124.6468,
        "rating": 4.3,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    
    # ADDITIONAL PLACES - You can add more here
    
    # MORE MALLS
    {
        "name": "SM City Cagayan de Oro",
        "category": "Mall",
        "type": "Mall",
        "description": "Large shopping complex with multiple floors, cinemas, and food court.",
        "latitude": 8.4760,
        "longitude": 124.6430,
        "lat": 8.4760,
        "lng": 124.6430,
        "rating": 4.5,
        "address": "C.M. Recto Avenue, Cagayan de Oro City",
        "price_range": "$$"
    },
    
    # MORE RESTAURANTS
    {
        "name": "Jollibee Cagayan de Oro",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Popular fast-food chain serving Filipino-style fried chicken and burgers.",
        "latitude": 8.4815,
        "longitude": 124.6475,
        "lat": 8.4815,
        "lng": 124.6475,
        "rating": 4.3,
        "address": "Centrio Mall, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "McDonald's CDO",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "International fast-food chain with local favorites.",
        "latitude": 8.4825,
        "longitude": 124.6480,
        "lat": 8.4825,
        "lng": 124.6480,
        "rating": 4.2,
        "address": "SM Downtown Premier, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "KFC Cagayan de Oro",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Famous fried chicken restaurant chain.",
        "latitude": 8.4805,
        "longitude": 124.6465,
        "lat": 8.4805,
        "lng": 124.6465,
        "rating": 4.3,
        "address": "Gaisano Mall, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "Chowking",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Chinese fast-food chain serving noodles, dimsum, and rice meals.",
        "latitude": 8.4795,
        "longitude": 124.6455,
        "lat": 8.4795,
        "lng": 124.6455,
        "rating": 4.1,
        "address": "Robinsons Cagayan de Oro",
        "price_range": "$"
    },
    {
        "name": "Mang Inasal",
        "category": "Restaurant",
        "type": "Restaurant",
        "description": "Filipino restaurant chain known for unlimited rice and grilled chicken.",
        "latitude": 8.4785,
        "longitude": 124.6445,
        "lat": 8.4785,
        "lng": 124.6445,
        "rating": 4.4,
        "address": "Limketkai Mall, Cagayan de Oro City",
        "price_range": "$"
    },
    
    # MORE LANDMARKS
    {
        "name": "Gaston Park",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Historic park and recreational area in the heart of Cagayan de Oro.",
        "latitude": 8.4840,
        "longitude": 124.6460,
        "lat": 8.4840,
        "lng": 124.6460,
        "rating": 4.4,
        "address": "Divisoria, Cagayan de Oro City",
        "price_range": "Free"
    },
    {
        "name": "Macahambus Cave",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Historic cave and natural attraction with scenic views.",
        "latitude": 8.4900,
        "longitude": 124.6500,
        "lat": 8.4900,
        "lng": 124.6500,
        "rating": 4.6,
        "address": "Macahambus, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "Cagayan de Oro Museum",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Museum showcasing the rich history and culture of Cagayan de Oro.",
        "latitude": 8.4850,
        "longitude": 124.6470,
        "lat": 8.4850,
        "lng": 124.6470,
        "rating": 4.5,
        "address": "City Hall Complex, Cagayan de Oro City",
        "price_range": "$"
    },
    {
        "name": "Golden Friendship Park",
        "category": "Landmark",
        "type": "Landmark",
        "description": "Beautiful park perfect for jogging, picnics, and family activities.",
        "latitude": 8.4865,
        "longitude": 124.6490,
        "lat": 8.4865,
        "lng": 124.6490,
        "rating": 4.3,
        "address": "Cagayan de Oro City",
        "price_range": "Free"
    },
    
    # MORE DORMS/HOTELS
    {
        "name": "N Hotel Cagayan de Oro",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Modern hotel with comfortable rooms and excellent amenities.",
        "latitude": 8.4810,
        "longitude": 124.6475,
        "lat": 8.4810,
        "lng": 124.6475,
        "rating": 4.4,
        "address": "Centrio Mall Area, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Mallberry Suites",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Boutique hotel offering stylish accommodations near shopping areas.",
        "latitude": 8.4790,
        "longitude": 124.6455,
        "lat": 8.4790,
        "lng": 124.6455,
        "rating": 4.5,
        "address": "Near Gaisano Mall, Cagayan de Oro City",
        "price_range": "$$"
    },
    {
        "name": "Pensionne La Florentina",
        "category": "Dorm/Hotel",
        "type": "Dorm/Hotel",
        "description": "Budget-friendly accommodation perfect for travelers.",
        "latitude": 8.4835,
        "longitude": 124.6470,
        "lat": 8.4835,
        "lng": 124.6470,
        "rating": 4.1,
        "address": "Divisoria Area, Cagayan de Oro City",
        "price_range": "$"
    }
]

def seed_database():
    """Clear existing data and insert sample places"""
    print("Clearing existing data...")
    collection.delete_many({})
    
    print(f"Inserting {len(places)} places...")
    result = collection.insert_many(places)
    
    print(f"Successfully inserted {len(result.inserted_ids)} places!")
    print("\nBreakdown by category:")
    
    categories = {}
    for place in places:
        cat = place['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  {cat}: {count} places")

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure MongoDB is running on localhost:27017")

