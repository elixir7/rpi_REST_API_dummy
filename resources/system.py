from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs
from machine import machine

class System(Resource):
    def get(self):
        system = machine.get("/api/v1/system").json()
        return jsonify(system)

system_api = Blueprint('resource.system', __name__)
api = Api(system_api)

api.add_resource(
    System,
    '/api/v1/system',
    endpoint = 'system'
)