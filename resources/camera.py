from flask import jsonify, Blueprint, send_file
from flask_restful import Resource, Api, reqparse, inputs
from machine import machine


class Camera(Resource):
    def get(self):
        camera = machine.get("/api/v1/camera").json()
        return jsonify(camera)

class Image(Resource):
    def get(self):
        filename = "http://192.168.100.110:8080/?action=snapshot.jpg"
        return send_file(filename, mimetype='image/jpg')
    

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