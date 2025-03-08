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
chairmen = db['local_gov_chairmen']

def find_chairman_email(state: str, lga: str):
    """
    Find the chairman's email given state and LGA.
    """
    state = state.strip().lower()
    lga = lga.strip().lower()

    result = chairmen.find_one({"state": state, "lga": lga})

    print(result)

    if result and 'email' in result and result['email'].strip():
        return result['email']

    return "No email found"

#Example test case (optional for direct running)
if __name__ == "__main__":
    # state = input("Enter state: ").strip()
    # lga = input("Enter LGA: ").strip()
    state = 'abiatest'
    lga = 'testlga'

    email = find_chairman_email(state, lga)
    print(f"Chairman's email for {lga}, {state}: {email}")
