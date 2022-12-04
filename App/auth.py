from datetime import date
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .model import check_user_exists, check_user_login, insert_user

auth = Blueprint("auth", __name__)
CORS(auth)

user_data = {}
user_exists={}

today = date.today()

@auth.route("/app/check-email", methods=['POST', 'GET'])
def check_email():
    if request.method =='POST': 
        data = request.json
        email = data['email']
        # print(email)
        user_exists.update({'status': check_user_exists(email)})
        # print(f"POST: {user_exists}")
    elif request.method =='GET':
        print("running get")
        return user_exists
    return "checking email tingz"
    
@auth.route("/app/signup", methods=['POST',"GET"])
def signup():
    if request.method == 'POST':
        user_data.clear()
        data = request.json
        user_data.update({
            "email" :data["email"],
            "name":data["name"],
            "date_joined": today.strftime("%B %d, %Y")
        })
        insert_user(
            data["name"], 
            data["email"], 
            data['password'],
            today.strftime("%B %d, %Y"),
            )
        return user_data
    else:
        return user_data
    

@auth.route("/app/login", methods=['POST',"GET"])
def login():
    if request.method == 'POST':
        user_data.clear()
        data = request.json
        # print(data['email'])
        # print(data['password'].strip())
        user_data.update(check_user_login(data['email'].strip(), data['password'].strip()))
        # print(check_user_login(data['email'].strip(), data['password'].strip()))
    else:
        return user_data
    return "login tingz"

   

