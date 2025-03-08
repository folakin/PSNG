import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection details
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

# Connection URI for Atlas
uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB_NAME}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[MONGO_DB_NAME]
geography_collection = db['lga_geography']
chairmen_collection = db['local_gov_chairmen']

def debug_geography():
    print("🔎 Debugging `lga_geography` Collection:")

    # Basic connection check
    try:
        client.admin.command('ping')
        print("✅ Connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Count documents
    try:
        count = geography_collection.count_documents({})
        print(f"✅ `lga_geography` contains {count} documents.")
    except Exception as e:
        print(f"❌ Failed to count documents: {e}")
        return

    # Sample document
    try:
        sample = geography_collection.find_one()
        print(f"✅ Sample document from `lga_geography`: {sample}")
    except Exception as e:
        print(f"❌ Failed to fetch sample document: {e}")
        return

    # Indexes
    try:
        indexes = geography_collection.index_information()
        print(f"✅ Indexes on `lga_geography`: {indexes}")
    except Exception as e:
        print(f"❌ Failed to fetch index information: {e}")
        return

def debug_chairmen():
    print("\n🔎 Debugging `local_government_chairmen` Collection:")

    try:
        sample_chair = chairmen_collection.find_one()
        print("Sample chairmen", sample_chair)
    except Exception as e:
        print(f'issue with chairmen db')
        return

    try:
        count = chairmen_collection.count_documents({})
        print(f"✅ `local_government_chairmen` contains {count} documents.")
    except Exception as e:
        print(f"❌ Failed to count documents: {e}")
        return

    try:
        sample = chairmen_collection.find_one()
        print(f"✅ Sample document from `local_government_chairmen`: {sample}")
    except Exception as e:
        print(f"❌ Failed to fetch sample document: {e}")
        return

    try:
        indexes = chairmen_collection.index_information()
        print(f"✅ Indexes on `local_government_chairmen`: {indexes}")
    except Exception as e:
        print(f"❌ Failed to fetch index information: {e}")
        return

if __name__ == "__main__":
    print("🚀 Running MongoDB Debugging Script")
    debug_geography()
    debug_chairmen()
