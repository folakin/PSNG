from flask import Flask, jsonify
from find_lga import find_lga_by_street, geography
from find_chairman import find_chairman_email
from send_complaint import process_complaint

app = Flask(__name__)

@app.route('/streets', methods=['GET'])
def get_all_streets():
    all_streets = set()

    cursor = geography.find({}, {'streets':1})
    for entry in cursor:
        all_streets.update(entry['streets'])

    return jsonify(sorted(list(all_streets)))

def main():
    street = input("Enter your street: ").strip().lower()

    lga, state = find_lga_by_street(street)

    if lga == "Unknown":
        print(f"⚠️ Could not find which LGA '{street}' belongs to.")
        return

    print(f"✅ Street belongs to {lga} LGA, {state} State.")

    chairman_email = find_chairman_email(state, lga)
    if chairman_email == "No email found":
        print(f"⚠️ No email found for Chairman of {lga} LGA.")
        return
    else:
        print(f"✅ Chairman's email: {chairman_email}")

    complaint_text = input("Please enter the issue you are facing, direct to the issue. NO DEGRADATION: ")
    process_complaint(state,lga,street,complaint_text,chairman_email)

if __name__ == "__main__":
    main()
