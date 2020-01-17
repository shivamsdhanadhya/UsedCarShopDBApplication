from usedcarapp import app
from flask import render_template, request, jsonify
from usedcarapp.service import LoginService

@app.route("/")
@app.route("/usedcarsshop")
@app.route("/usedcarsshop/<car>")
def index(car='car1'):
    #return "<h1>Hello Team 60, welcome to Used Car Shop </h1>"
    car_data = {"car1": "Honda City", "car2": "Eco Sport"}
    car = car_data[car]
    print(car_data)
    return render_template("index.html", car_data=car_data, car=car)

@app.route("/templates/view_car.html")
def view_car():
    id = request.args.get('car1')
    return render_template("view_car.html", data={"id": id})

@app.route("/usedcarsshop/login", methods=['POST'])
def login():
    payload = request.get_json()
    username = payload['username']
    password = payload['password']
    login_service = LoginService()
    return jsonify(login_service.login(username,password))