from flask import Blueprint, request, jsonify
from pymongo import errors
from bson.objectid import ObjectId
from server.db import users_collection
import logging

users_bp = Blueprint("users", __name__)

logging.basicConfig(level=logging.INFO)

def handle_pymongo_error(e):
    logging.error(f"PyMongoError: {str(e)}")
    return jsonify({"error": "Database error occurred"}), 500

@users_bp.route("/", methods=["GET"])
def get_users():
    try:
        users = []
        for user in users_collection.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        return jsonify(users), 200
    except errors.PyMongoError as e:
        return handle_pymongo_error(e)
    
@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    except errors.InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400
    except errors.PyMongoError as e:
        return handle_pymongo_error(e)
    
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        
        result = users_collection.insert_one(data)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        new_user["_id"] = str(new_user["_id"])
        return jsonify(new_user), 201
    except errors.PyMongoError as e:
        return handle_pymongo_error(e)

@users_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        if result.modified_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
        updated_user["_id"] = str(updated_user["_id"])
        return jsonify(updated_user), 200
    except errors.InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400
    except errors.PyMongoError as e:
        return handle_pymongo_error(e)
    
@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"message": "User deleted"}), 200
    except errors.InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400
    except errors.PyMongoError as e:
        return handle_pymongo_error(e)