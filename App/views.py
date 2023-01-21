from flask import Blueprint, request
from flask_cors import CORS

from .model import upload_image

views = Blueprint("views", __name__)
CORS(views)

@views.route("/upload/img_detail", methods=['GET', 'POST'])
def email():
    if(request.method == "POST"):
        try:
            email = request.json['email']
            time = request.json['time']
       
            date = request.json['date']
        
            actual_location = request.json['actual_location']
       
            img_id = request.json['img_id']
        
            img_filename = request.json['img_filename']

            upload_image(email, img_id, img_filename, time, date, actual_location)
        except:
            upload_image(request.json['email'], request.json['img_id'], request.json['img_filename'])
        
        
        

        
      
        return "success"


