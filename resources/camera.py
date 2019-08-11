from flask import jsonify, Blueprint, send_file
from flask_restful import Resource, Api, reqparse
from printers import printerList
from werkzeug.contrib.cache import SimpleCache
from clint.textui import puts, colored

import requests

cache = SimpleCache()

class Camera(Resource):
    def get(self):
        cameraList = list()
        for printer in printerList.getPrinters():
            r = printer.get("api/v1/camera")
            if r:
                camera_link = r.json()
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
            for printer in printerList.getPrinters():
                imageLink = "http://" + printer.getIp() + ":8080/?action=snapshot.jpg"
                imageLinks.append(imageLink)
            #long timeout, the links should not update....
            cache.set("images", imageLinks, timeout=60*60)
            images = cache.get("images")
        

        parser = reqparse.RequestParser()
        parser.add_argument('printer', type=int, required=True)
        args = parser.parse_args()
        printer_numb = args["printer"]

        if printer_numb not in range(0, len(printerList.getPrinters())): 
            msg = jsonify({
                "printer": "Only a ID between 0 and " + str(len(printerList.getPrinters()) - 1) + " is valid"
            })
            return msg

        img_data = requests.get(images[printer_numb]).content

        for i, printer in enumerate(printerList.getPrinters()):
            if i == printer_numb:
                printer_name = printer.getName()

        filePath = "images/"  + printer_name + "_snapshot.jpg"
        with open(filePath, 'wb') as handler:
            handler.write(img_data)

        return send_file(filePath)
    #Saveing the images is done but every request we do a new save....

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