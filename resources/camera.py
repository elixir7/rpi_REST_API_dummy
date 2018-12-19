from flask import jsonify, Blueprint, send_file
from flask_restful import Resource, Api, reqparse
from printers import printers
from werkzeug.contrib.cache import SimpleCache
from clint.textui import puts, colored

import requests

cache = SimpleCache()

class Camera(Resource):
    def get(self):
        cameraList = list()
        for printer in printers:
            camera_link = printer.get("/api/v1/camera").json()
            cameraList.append(camera_link)
        return jsonify(cameraList)

class Image(Resource):
    def get(self):
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('printer', type=int)
        args = parser.parse_args()
        print("parser: ")
        print(args)
        '''
        
        images = cache.get("images")
        if images is None:
            imageLinks = list()
            for printer in printers:
                imageLink = "http://" + printer.getIp() + ":8080/?action=snapshot.jpg"
                imageLinks.append(imageLink)
            #long timeout, the links should not update....
            cache.set("images", imageLinks, timeout=60*60)
            images = cache.get("images")
        

        parser = reqparse.RequestParser()
        parser.add_argument('printer', type=int)
        args = parser.parse_args()
        printer_numb = args["printer"]
        puts(colored.red(str(printer_numb)))

        img_data = requests.get(images[printer_numb]).content

        filePath = "images/"  + str(printers[printer_numb].get("name")) + "_snapshot.jpg"
        with open(filePath, 'wb') as handler:
            handler.write(img_data)

        return send_file(filePath)
    #Savint the images is done but every request we do a new save....

camera_api = Blueprint('resource.camera', __name__)
api = Api(camera_api)

api.add_resource(
    Camera,
    '/api/v1/camera',
    endpoint = 'camera'
)
api.add_resource(
    Image,
    '/api/v1/camera/image',
    endpoint = 'image'
)