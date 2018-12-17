from flask import jsonify, Blueprint, send_file, request
from flask_restful import Resource, Api, reqparse, inputs
from printers import printers


class Camera(Resource):
    def get(self):
        cameraList = list()
        for printer in printers:
            camera_link = printer.get("/api/v1/camera").json()
            cameraList.append(camera_link)
        return jsonify(cameraList)

class Image(Resource):
    def get(self):
        args = request.args
        print (args) # For debugging

        #Getting an image should require a parameter in the URL which tells what printer to take a picture
        #Try this request.args https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request

        #imgList = list()
        #for printer in printers:
        #    img_link = printer.get("")
        #filename = "http://192.168.100.110:8080/?action=snapshot.jpg"
        #return send_file(filename, mimetype='image/jpg')
    

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