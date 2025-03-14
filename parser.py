import json
import datetime
from dataclasses import dataclass, asdict
from typing import List
from pymongo import MongoClient, errors
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    created_ts: float
    active: bool = True

def parse_roles(item: dict) -> List[str]:
    """Translate booleans into role strings"""
    roles = []
    if item.get("is_user_admin"):
        roles.append("admin")
    if item.get("is_user_manager"):
        roles.append("manager")
    if item.get("is_user_tester"):
        roles.append("tester")
    return roles

def parse_iso_to_timestamp(iso_str: str) -> float:
    """Convert ISO 8601 string to a Unix timestamp"""
    try:
        return datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00")).timestamp()
    except ValueError as e:
        logging.error(f"Error parsing date: {iso_str} - {e}")
        return 0.0

def main():
    try:
        # Load JSON data
        with open("udata.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return

    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users_collection = db["users"]
    except errors.ConnectionError as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return

    # Parse JSON data and insert into MongoDB
    for item in data.get("users", []):
        try:
            user_obj = User(
                username=item["user"],
                password=item["password"],
                roles=parse_roles(item),
                preferences=UserPreferences(timezone=item["user_timezone"]),
                created_ts=parse_iso_to_timestamp(item["created_at"])
            )
            users_collection.insert_one(asdict(user_obj))
        except KeyError as e:
            logging.error(f"Missing key in data: {e}")
        except errors.PyMongoError as e:
            logging.error(f"Error inserting data into MongoDB: {e}")

    logging.info("Data inserted successfully into 'users' collection")

if __name__ == "__main__":
    main()