from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from printers import printers
from clint.textui import puts, colored
from werkzeug.contrib.cache import SimpleCache

import json

cache = SimpleCache()

class ESP8266(Resource):
    def get(self):
        espData = cache.get("espData")
        if espData is None:
            puts(colored.cyan("Getting new esp data!"))
            espData = json.load(open("esp8266_data.json", "rt"))
            cache.set("espData", espData, timeout=5)
            espData = cache.get("espData")
        return jsonify(espData)

esp8266_api = Blueprint('resource.esp8266', __name__)
api = Api(esp8266_api)

api.add_resource(
    ESP8266,
    '/api/v1/esp',
    endpoint = 'esp8266'
)
