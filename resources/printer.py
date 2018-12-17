from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs
from clint.textui import colored, puts

class Printer(Resource):
    def get(self):
        dummyJSON = {
            "bed": {
                "temperature":{
                    "current": "240",
                    "target": "245"
                }
            },
            "led": {
                "brightness": "100",
                "saturation": "50",
                "hue": "20"
            },
            "status": "idle"
        }
        return jsonify(dummyJSON)

printer_api = Blueprint('resource.printer', __name__)
api = Api(printer_api)

api.add_resource(
    Printer,
    '/api/v1/printer',
    endpoint = 'printer'
)