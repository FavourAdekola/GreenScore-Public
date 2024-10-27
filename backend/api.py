import os
from dotenv import load_dotenv, dotenv_values 

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv() 

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://greenscore.pages.dev",  # Your Cloudflare Pages domain
            "http://localhost:3000"        # Local development
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
uri = os.getenv("MONGODB_URI")

# Initialize MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['data']
users_collection = db['users']

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")  # Replace with your Google Client ID


# Update your existing routes to include proper headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route('/auth/google', methods=['POST'])
def google_auth():
    try:
        # Get only the user info fields we want to update
        user_info = {
            'google_id': request.json['google_id'],
            'email': request.json['email'],
            'name': request.json['name'],
            'picture': request.json['picture'],
        }

        # First, check if user exists and get their current points
        existing_user = users_collection.find_one({'google_id': user_info['google_id']})
        
        if existing_user:
            # If user exists, preserve their points
            result = users_collection.update_one(
                {'google_id': user_info['google_id']},
                {'$set': user_info}  # Only update user info, not points
            )
            user = users_collection.find_one({'google_id': user_info['google_id']})
        else:
            # If new user, initialize with 0 points
            user_info['points'] = 0
            users_collection.insert_one(user_info)
            user = user_info

        # Convert ObjectId to string for JSON serialization
        if '_id' in user:
            user['_id'] = str(user['_id'])

        return jsonify(user)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/user/<google_id>/points', methods=['GET'])
def get_user_points(google_id):
    try:
        user = users_collection.find_one({'google_id': google_id})
        if user:
            return jsonify({'points': user.get('points', 0)})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<google_id>/points', methods=['POST'])
def update_user_points(google_id):
    try:
        points = request.json.get('points', 0)
        
        result = users_collection.update_one(
            {'google_id': google_id},
            {'$set': {'points': points}}
        )
        
        if result.modified_count > 0:
            return jsonify({'success': True, 'points': points})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add this to your existing app.py

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        # Get limit from query params, default to 10
        limit = int(request.args.get('limit', 10))
        
        # Get users sorted by points in descending order
        leaderboard = list(users_collection.find(
            {},  # Query all users
            {
                '_id': 0,  # Exclude _id field
                'google_id': 1,
                'name': 1,
                'picture': 1,
                'points': 1
            }
        ).sort('points', -1).limit(limit))
        
        # Ensure points exists for all users
        for user in leaderboard:
            if 'points' not in user:
                user['points'] = 0

        return jsonify(leaderboard)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)