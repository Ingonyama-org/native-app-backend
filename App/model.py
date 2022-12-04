import os
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
user_collection = ingonyama_app_db.user

def insert_user(name, email, password, date_joined):
    user = {
        "name": name, 
        "email":email.lower(),
        "date_joined":date_joined,
        "password":generate_password_hash(password,method="sha256")
        }
    user_collection.insert_one(user)
# insert_user("LUms","luna@gmail.com","Kenya","+254712345678","Nairobi", "13th Aug 2022","I am Deaf","12345678")


def check_user_exists(email):
    user = user_collection.find_one({'email':email.lower()})
    if user:
        return True
    else:
        return False
# print(check_user_exists("LUMONA@gmail.com"))

def upload_image():
    #Create a object of GridFs for the above database.
    fs = gridfs.GridFS(database)

    #define an image object with the location.
    file = "C:/Users/user/Pictures/dog.jpeg"

    #Open the image in read-only format.
    with open(file, 'rb') as f:
        contents = f.read()

    #Now store/put the image via GridFs object.
    fs.put(contents, filename="file")
    

def check_user_login(email,pwd):
    user_details = {}
    user = user_collection.find_one({"email":email})
    # print(user)
    if user:
        if check_password_hash(user['password'], pwd):
            user_details.update({
                "name": user['name'], 
                "email": user['email'],
                "date_joined":user["date_joined"] 
                })
            return user_details
        else: 
            return user_details
    else: 
        return user_details
    
# print(check_user_login("luna@gmail.com", 'abcdefgh'))

def update_user_details(id, email, password, name ):
    new_value={
        "name": name, 
        "email":email,
        "password":generate_password_hash(password,method="sha256")
        }
    all_update = {
        "$set": new_value
        }
    user_collection.update_one({'key': id}, all_update)


        
    