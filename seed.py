import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

#load env
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("MONGO_DB_NAME")
cluster = os.getenv("MONGO_CLUSTER")

uri = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client[db_name]

chairmen = db['local_gov_chairmen']
geography = db['lga_geography']


def seed_chairmen():
    """Reads lgas_chairmen.csv and inserts into local_government_chairmen collection."""
    chairmen.drop()  # Clear old data
    with open('lgas_chairmen.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            data.append({
                "state": row['state'],
                "lga": row['lga'],
                "chairman_name": row['chairman_name'],
                "email": row['email'],
                "assumed_office": row['assumed_office'],
                "term_end": row['term_end'],
                "notes": row['notes']
            })
        chairmen.insert_many(data)
    print(f"✅ Seeded {len(data)} chairmen into MongoDB Atlas.")
def seed_geography():
    """Reads lga_geography.csv and inserts into lga_geography collection."""
    geography.drop()  # Clear old data
    with open('lga_geography.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            streets = [street.strip() for street in row['streets'].split(',') if street.strip()]
            data.append({
                "state": row['state'],
                "lga": row['lga'],
                "streets": streets
            })
        geography.insert_many(data)
    geography.create_index([("streets", 1)])
    print(f"✅ Seeded {len(data)} geography entries into MongoDB Atlas.")

if __name__ == "__main__":
    seed_chairmen()
    seed_geography()
    print("✅ All data seeded successfully.")


