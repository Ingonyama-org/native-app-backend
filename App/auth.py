import base64
from datetime import date
from io import BytesIO
from time import sleep
import time
from urllib import response
from flask import Blueprint, request
from PIL import Image
from flask_cors import CORS, cross_origin
from .model import check_user_exists, check_user_login, insert_user, fs, check_password_matches, update_user_details

auth = Blueprint("auth", __name__)
CORS(auth)

user_data = {}
img_data = {}
user_exists={}

today = date.today()

@auth.route("/app/check-email", methods=['POST', 'GET'])
def check_email():
    if request.method =='POST': 
        data = request.json
        email = data['email'].lower()
        # print(email)
        user_exists.update({'status': check_user_exists(email)})
        # print(f"POST: {user_exists}")
    elif request.method =='GET':
        print("running get")
        return user_exists
    return "checking email tingz"

@auth.route("/app/check-password", methods=['POST'])
def check_password():
    data = request.json
    email = data['email'].lower()
    pwd = data['pwd']
   
    return {'status': check_password_matches(email, pwd)}
    
@auth.route("/app/signup", methods=['POST',"GET"])
def signup():
    if request.method == 'POST':
        user_data.clear()
        data = request.json
        print(data)
        user_data.update({
            "email" :data["email"].lower(),
            "name":data["name"],
            "date_joined": today.strftime("%B %d, %Y"),
            "age": data['age'],
            "gender": data['gender'],
            "nationality": data['nationality']
        })
       
        insert_user(
            data["name"], 
            data["email"].lower(), 
            data["age"],
            data['gender'],
           data['nationality'],
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
        user_data.update(check_user_login(data['email'].strip(), data['password'].strip()))
    else:
        return user_data
    return "login tingz"


@auth.route('app/update', methods=['POST', 'GET'])
def user_profile_edit():
    data = request.json
    user_details = update_user_details(data["email"], data['name'], data['password'])
    print(user_details)

    return user_details