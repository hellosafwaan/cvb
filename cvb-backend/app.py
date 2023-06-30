from datetime import date
from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from settings import MONGO_URI

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client["cvb"]
admin_users_col = db["admin_users"]
vacc_centers_col = db["vacc_centers"]
users_col = db["users"]


@app.route("/ping", methods=["POST", "GET"])
def ping():
    return jsonify({"message": "Hello World!"})


@app.route("/admin/auth", methods=["POST"])
def adminAuth():
    payload = request.get_json()

    username = payload["username"]
    password = payload["password"]

    data = admin_users_col.find_one({"username": username})

    if data is None:
        return jsonify({"message": "Invalid username or password"}), 401

    if data["password"] == password:
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.route("/user/auth", methods=["POST"])
def userAuth():
    payload = request.get_json()

    username = payload["username"]
    password = payload["password"]

    data = users_col.find_one({"username": username})

    if data is None:
        return jsonify({"message": "Invalid username or password"}), 401

    if data["password"] == password:
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401


# @app.route("/admin/addvacc", methods=["POST"])
# def addvacc():
#     payload = request.get_json()

#     data = vacc_centers_col.insert_one(payload)

#     return jsonify({"message": "Vaccination center added successfully"}), 200



@app.route("/admin/addvacc", methods=["POST"])
def addvacc():
    payload = request.get_json()

    # name = payload.get("name")
    # address = payload.get("address")
    # phone = payload.get("phone")
    # pincode = payload.get("pincode")
    # dosage = payload.get("dosage")
    # start_time = payload.get("start_time")
    # end_time = payload.get("end_time")

    # # Validate the input fields
    # if not name or not address or not phone or not pincode or not dosage or not start_time or not end_time:
    #     return jsonify({"message": "All fields are required"}), 400

    # # Check if the vaccination center already exists
    # existing_center = vacc_centers_col.find_one({"name": name})
    # if existing_center:
    #     return jsonify({"message": "Vaccination center already exists"}), 409

    # Create a new vaccination center document
    # new_center = {
    #     "name": name,
    #     "address": address,
    #     "phone": phone,
    #     "pincode": pincode,
    #     "dosage": dosage,
    #     "working_hours": {
    #         "start_time": start_time,
    #         "end_time": end_time
    #     },
    #     "slots_booked": {}
    # }

    # Insert the new vaccination center into the collection
    vacc_centers_col.insert_one(payload)
    return jsonify({"message": "Vaccination center added successfully"}), 200






# @app.route("/user/slotbook", methods=["POST"])
# def slotbook():
#     payload = request.get_json()

#     centre_name = payload["centre_name"]

#     data = vacc_centers_col.find_one({"name": centre_name})

#     if data is None:
#         return jsonify({"message": "Invalid vaccination center name"}), 401

#     data["dosage"] = str(int(data["dosage"]) - 1)

#     vacc_centers_col.update_one({"name": centre_name}, {"$set": data})

#     return jsonify({"message": "Vaccination center Booked successfully"}), 200




@app.route("/user/slotbook", methods=["POST"])
def slotbook():
    payload = request.get_json()
    print(payload)
    centre_name = payload["centre_name"]
    booking_date = payload["booking_date"]

    # Convert the booking_date string to a datetime object
    try:
        booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid booking date format. Please select a valid date."}), 400

    # Check if the selected vaccination center exists
    data = vacc_centers_col.find_one({"name": centre_name})
    if data is None:
        return jsonify({"message": "Invalid vaccination center name"}), 401

    # Get the current date
    today = date.today()

    # Check if the selected booking date is in the past
    if booking_date < today:
        return jsonify({"message": "Cannot book slots for a past date. Please select a valid date."}), 400

    # Check the number of slots already booked for the selected date
    slots_booked = data.get("slots_booked", {}).get(str(booking_date), 0)
    print(slots_booked)
    if slots_booked >= 10:
        return jsonify({"message": "No available slots for the selected date. Please choose another date."}), 200

    # Increment the slots booked count for the selected date
    vacc_centers_col.update_one({"name": centre_name}, {"$inc": {f"slots_booked.{booking_date}": 1}})

    return jsonify({"message": "Vaccination center booked successfully"}), 200



@app.route("/admin/removevacc", methods=["POST"])
def removevacc():
    payload = request.get_json()

    centre_name = payload["centre_name"]

    data = vacc_centers_col.delete_one({"name": centre_name})

    return jsonify({"message": "Vaccination center removed successfully"}), 200


@app.route("/admin/getdosage", methods=["POST", "GET"])
def getdosage():
    list_of_vacc_centres = vacc_centers_col.find()

    final_result = []

    for centre in list_of_vacc_centres:
        current = {
            "name": centre["name"],
            "dosage": centre["dosage"],
        }

        final_result.append(current)

    return jsonify(final_result), 200


@app.route("/admin/getvacc", methods=["POST", "GET"])
def getvacc():
    list_of_vacc_centres = vacc_centers_col.find()

    final_result = []

    for centre in list_of_vacc_centres:
        del centre["_id"]

        final_result.append(centre)

    return jsonify(final_result), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
