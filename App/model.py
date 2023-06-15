import os
import cv2
import time
import gridfs
import certifi
import numpy as np
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

# initialize GridFS
fs = gridfs.GridFS(ingonyama_app_db, collection="uploaded_img")

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

# GETING ALL THE COORDINATES
def get_coordinates():
    coordinates = []
    id_count = 0
    for document in img_detail_collection.find():
        actual_location = document.get("actual_location")
        if actual_location:
            if isinstance(actual_location, list) and len(actual_location) > 0:
                coords = actual_location[0].get("coords")
                if coords:
                    latitude = coords.get("latitude")
                    longitude = coords.get("longitude")
                    if latitude is not None and longitude is not None:
                        coordinates.append({"id": id_count, "latitude": latitude, "longitude": longitude})
                        id_count +=1
    return coordinates


def save_images_to_folder():
    # Create the folder if it doesn't exist
    folder_path = "uploaded_images"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
 
    # Retrieve the image documents from the collection
    image_documents = ingonyama_app_db["uploaded_img.files"].find({})

    # Iterate over the image documents and save the images to the folder
    for document in image_documents:
        image_id = document["_id"]
        image_filename = document["filename"]
        image_data = fs.get(image_id).read()

        # Generate the file path for saving the image
        file_path = os.path.join(folder_path, image_filename)

        # Save the image to the specified folder
        with open(file_path, "wb") as file:
            file.write(image_data)

    print("Images saved to folder: uploaded_images")


# save_images_to_folder()
