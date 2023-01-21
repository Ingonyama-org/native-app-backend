import os
import time
import certifi

import gridfs
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

load_dotenv(find_dotenv())
password = os.environ.get('MONGO_PWD')

connection_string = f"mongodb+srv://lumona:{password}@ingonyama.mhjrkw1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())
ingonyama_app_db = client.ingonyama_app_dbl
fs = gridfs.GridFS(ingonyama_app_db)
user_collection = ingonyama_app_db.user
img_detail_collection = ingonyama_app_db.details_img_uploaded

def insert_user(name, email, phone_number, password, date_joined):
    user = {
        "name": name, 
        "email":email.lower(),
        "phone_number":phone_number,
        "date_joined":date_joined,
        "password":generate_password_hash(password,method="sha256")
        }
    user_collection.insert_one(user)

def check_user_exists(email):
    user = user_collection.find_one({'email':email.lower()})
    if user:
        return True
    else:
        return False

def check_password_matches(email, pwd):
    user = user_collection.find_one({'email':email.lower()})
    if user:
        if check_password_hash(user['password'], pwd):
            return True
        else: 
            return False
    else:
        return False

def upload_image(email, img_id, img_filename, time="undefined", date="undefined", actual_location="undefined"):
    user = user_collection.find_one({'email':email.lower()})

    if user:
        img_detail = {
            "email":email,
            "img_id": img_id, 
            "img_filename": img_filename,
            "time": time,
            "date":date,
            "actual_location":actual_location
        }
        img_detail_collection.insert_one(img_detail)


def check_user_login(email,pwd):
    user_details = {}
    user = user_collection.find_one({"email":email.lower()})
    if user:
        if check_password_hash(user['password'], pwd):
            # img_uploads = img_detail_collection.find_one({'email':email.lower()})
            # if img_uploads:
            #     for img_doc in img_detail_collection.find({'email': email.lower()}):
            #         img_id = ObjectId(img_doc['img_id'])
            #         storage = gridfs.GridFS(ingonyama_app_db, "fs")
            #         print(storage.get(file_id=img_id))
            #         try:
            #             fileobj = storage.get(file_id=ObjectId(img_id))
            #             print(fileobj)
            #         except:
            #             pass
   

                
            user_details.update({
                "name": user['name'], 
                "email": user['email'],
                "date_joined":user["date_joined"],
                # "img_data":fs.get(user_img_upload["img_id"]).read(),
                # "img_url":f'{request.url_root}auth/app/upload/img/{user_img_upload["img_id"]}',
                # "time":user_img_upload['time'],
                # 'date':user_img_upload['date'],
                # 'actual_location':user_img_upload['actual_location']
                })
          
            return user_details
        else: 
            return user_details
    else: 
        return user_details
    

def update_user_details(email, name, password):
    user =user_collection.find_one({"email": email.lower()})
    if user:
        new_value={
            "name": name, 
            "email":email.lower(),
            "password":generate_password_hash(password,method="sha256") if password else user['password']
            }
        all_update = {
            "$set": new_value
            }
        user_collection.update_one({'email': email}, all_update)
        time.sleep(2.4)
        return {"name": user['name'],"email": user['email'],"phone_number":user["phone_number"], "date_joined":user['date_joined']}

def get_user_by_email(email):
    user = user_collection.find_one({'email':email})
    return user    






        
    