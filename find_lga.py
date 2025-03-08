from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection details
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("MONGO_DB_NAME")
cluster = os.getenv("MONGO_CLUSTER")

# Connection URI for Atlas
uri = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[db_name]
geography = db['lga_geography']

def find_lga_by_street(street_name: str):
    """
    Find the LGA and State given a street name, querying directly from MongoDB Atlas.
    """
    street_name = street_name.strip().lower()

    # Search for any document where the street appears in the 'streets' array (case insensitive match)
    #result = geography.find_one({"streets": {"$regex": f"^{street_name}$", "$options": "i"}})
    result = geography.find_one({
        "streets": street_name
    })

    if result:
        return result['lga'], result['state']

    # Not found
    return "Unknown", "Unknown"

# Example test case (only runs when directly executed for quick test purposes)
# if __name__ == "__main__":
#
#     street = input("Please input your street: ")
#
#     count = geography.count_documents({})
#     print(f"geography has {count}")
#
#
#     indexes = geography.index_information()
#     print(indexes)
#
#
#     lga, state = find_lga_by_street(street)
#     if lga == "Unknown":
#         print(f"⚠️ Could not find LGA for '{street}'.")
#     else:
#         print(f"✅ '{street}' belongs to {lga} LGA, {state} State.")
