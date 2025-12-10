from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import math
import os
import requests
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, static_folder='../', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # In production, replace with your frontend URL
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client["taracdo_db"]
    collection = db["establishments"]
    users_collection = db["users"]
    client.server_info()  # Test connection
    print("Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    print("Make sure MongoDB is running or MONGODB_URI is set correctly")

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except:
                return jsonify({"error": "Invalid token format"}), 401
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_collection.find_one({"email": data['email']})
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Helper function to convert MongoDB documents
def serialize(doc):
    if doc and '_id' in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# Calculate distance between two coordinates (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c  # Distance in meters

# Serve static files
@app.route('/')
def index():
    return send_from_directory('../', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)

# API Routes
@app.route('/api/establishments', methods=['GET'])
def get_all():
    # Make authentication optional for establishments (for map to work)
    try:
        data = list(collection.find())
        return jsonify([serialize(d) for d in data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/establishments', methods=['POST'])
def add_establishment():
    try:
        data = request.json
        result = collection.insert_one(data)
        new_item = collection.find_one({"_id": result.inserted_id})
        return jsonify(serialize(new_item)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/establishments/<id>', methods=['GET'])
def get_one(id):
    try:
        doc = collection.find_one({"_id": ObjectId(id)})
        if doc:
            return jsonify(serialize(doc)), 200
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/establishments/<id>', methods=['PUT'])
def update(id):
    try:
        data = request.json
        updated = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        
        if updated.matched_count == 0:
            return jsonify({"error": "Not found"}), 404
        
        doc = collection.find_one({"_id": ObjectId(id)})
        return jsonify(serialize(doc)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/establishments/<id>', methods=['DELETE'])
def delete(id):
    try:
        deleted = collection.delete_one({"_id": ObjectId(id)})
        if deleted.deleted_count == 0:
            return jsonify({"error": "Not found"}), 404
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Geocoding endpoint - reverse geocode coordinates to address (optional auth)
@app.route('/api/geocode', methods=['GET'])
def geocode():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        # Use Nominatim (OpenStreetMap) for reverse geocoding with higher zoom for better accuracy
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18&addressdetails=1&accept-language=en"
        headers = {'User-Agent': 'TaraCDO/1.0 (contact@taracdo.com)'}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            addr = data.get('address', {})
            
            # Build a more accurate address for Cagayan de Oro
            parts = []
            
            # Try to get specific area/barangay first
            if addr.get('neighbourhood'):
                parts.append(addr.get('neighbourhood'))
            elif addr.get('suburb'):
                parts.append(addr.get('suburb'))
            elif addr.get('village'):
                parts.append(addr.get('village'))
            elif addr.get('quarter'):
                parts.append(addr.get('quarter'))
            
            # Add road/street if available
            if addr.get('road'):
                parts.append(addr.get('road'))
            
            # Add city (should be Cagayan de Oro)
            city = addr.get('city') or addr.get('town') or addr.get('municipality')
            if city:
                parts.append(city)
            else:
                # If no city found, check if coordinates are within CDO bounds
                if 8.3 <= lat <= 8.6 and 124.5 <= lng <= 124.8:
                    parts.append('Cagayan de Oro City')
            
            # Add province/state
            if addr.get('state'):
                parts.append(addr.get('state'))
            
            if parts:
                address = ', '.join(parts)
            else:
                # Fallback to display_name
                address = data.get('display_name', f'Cagayan de Oro City (Lat: {lat:.6f}, Lng: {lng:.6f})')
            
            return jsonify({"address": address, "lat": lat, "lng": lng, "raw": addr}), 200
        else:
            return jsonify({"address": f"Cagayan de Oro City (Lat: {lat:.6f}, Lng: {lng:.6f})"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "address": f"Cagayan de Oro City (Lat: {lat:.6f}, Lng: {lng:.6f})"}), 200

# Nearby places endpoint (optional auth)
@app.route('/api/nearby', methods=['GET'])
def nearby():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5000))  # Default 5km
        
        # Get all establishments
        all_places = list(collection.find())
        
        # Calculate distance and filter
        nearby_places = []
        for place in all_places:
            place_lat = place.get('lat') or place.get('latitude')
            place_lng = place.get('lng') or place.get('longitude')
            
            if place_lat and place_lng:
                distance = calculate_distance(lat, lng, place_lat, place_lng)
                if distance <= radius:
                    place['distance'] = round(distance, 0)  # Distance in meters
                    nearby_places.append(place)
        
        # Sort by distance
        nearby_places.sort(key=lambda x: x.get('distance', float('inf')))
        
        return jsonify([serialize(p) for p in nearby_places]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "User already exists"}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = {
            "email": email,
            "password": hashed_password,
            "name": name,
            "created_at": datetime.datetime.utcnow()
        }
        
        result = users_collection.insert_one(user)
        user['_id'] = str(result.inserted_id)
        del user['password']
        
        # Generate token
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "message": "User created successfully",
            "token": token,
            "user": serialize(user)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Find user
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Generate token
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        user_data = serialize(user)
        del user_data['password']
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    user_data = serialize(current_user)
    del user_data['password']
    return jsonify(user_data), 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=port)