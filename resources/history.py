from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs
from machine import machine

class History(Resource):
    def get(self):
        print("Trying to get history")
        history = machine.get("/api/v1/history").json()
        print(history)
        return jsonify(history)

history_api = Blueprint('resource.history', __name__)
api = Api(history_api)

api.add_resource(
    History,
    '/api/v1/history',
    endpoint = 'history'
)