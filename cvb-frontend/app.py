from flask import Flask, render_template, request
from settings import HOST, PORT, BACKEND_URL
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def adminlog():
    return render_template("adminLogin.html")


@app.route("/user/login", methods=["GET", "POST"])
def userlog():
    return render_template("userLogin.html")


@app.route("/admin/dashboard", methods=["GET", "POST"])
def adminAuth():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        res = requests.post(
            BACKEND_URL + "/admin/auth",
            json={"username": username, "password": password},
        )

        if res.status_code == 200:
            return render_template("adminDashboard.html")

        return render_template(
            "adminLogin.html", alert_msg="Invalid username or password"
        )


@app.route("/user/dashboard", methods=["GET", "POST"])
def userAuth():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        res = requests.post(
            BACKEND_URL + "/user/auth",
            json={"username": username, "password": password},
        )

        if res.status_code == 200:
            return render_template("userDashboard.html")

        return render_template(
            "userLogin.html", alert_msg="Invalid username or password"
        )


@app.route("/admin/dashboard/addvacc", methods=["GET", "POST"])
def addVacc():
    if request.method == "POST":
        data = request.form

        res = requests.post(BACKEND_URL + "/admin/addvacc", json=data)

        if res.status_code == 200:
            return render_template(
                "addVacc.html", alert_msg="Vaccine added successfully"
            )

        return render_template("addVacc.html", alert_msg="Error adding vaccine")

    return render_template("addVacc.html")


@app.route("/admin/dashboard/removevacc", methods=["GET", "POST"])
def removevacc():
    all_vacc = requests.get(BACKEND_URL + "/admin/getvacc")

    if request.method == "POST":
        data = request.form

        res = requests.post(BACKEND_URL + "/admin/removevacc", json=data)

        if res.status_code == 200:
            return render_template(
                "removevacc.html", alert_msg="Vaccine removed successfully"
            )

        return render_template("removevacc.html", alert_msg="Error removing vaccine")

    return render_template("removevacc.html", vacc_centres=all_vacc.json())


@app.route("/admin/dashboard/getdosage", methods=["GET", "POST"])
def getDosage():
    res = requests.get(BACKEND_URL + "/admin/getdosage")

    if res.status_code == 200:
        return render_template("getDosage.html", data=res.json())

    return render_template("getDosage.html", alert_msg="Error fetching data")


@app.route("/user/dashboard/searchcentre", methods=["GET", "POST"])
def getvacc():
    res = requests.get(BACKEND_URL + "/admin/getvacc")

    if res.status_code == 200:
        return render_template("searchvacc.html", data=res.json())

    return render_template("searchvacc.html", alert_msg="Error fetching data")


@app.route("/user/dashboard/slotbook", methods=["GET", "POST"])
def slotbook():
    data_vacc = requests.get(BACKEND_URL + "/admin/getvacc")

    if request.method == "POST":
        data = request.form

        res = requests.post(BACKEND_URL + "/user/slotbook", json=data)
        msg = res.json()
        msg = msg['message']
        if res.status_code == 200:
            return render_template(
                "slotbook.html",
                alert_msg="Slot booked successfully",
                vacc_centres=data_vacc.json(),
            )

        return render_template(
            "slotbook.html", alert_msg= msg, vacc_centres=data_vacc.json()
        )

    return render_template("slotbook.html", vacc_centres=data_vacc.json())


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
