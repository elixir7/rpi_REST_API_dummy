from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from printers import printers
from clint.textui import puts, colored
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

class Printer(Resource):
    def get(self):
        printerData = cache.get("printerData")
        if printerData is None:
            puts(colored.cyan("Getting new Printer data!"))
            printerDataList = list()
            for printer in printers:
                data = printer.get("/api/v1/printer").json()
                printerDataList.append(data)
            cache.set("printerData", printerDataList, timeout=5)
            printerData = cache.get("printerData")
        return jsonify(printerData)

printer_api = Blueprint('resource.printer', __name__)
api = Api(printer_api)

api.add_resource(
    Printer,
    '/api/v1/printer',
    endpoint = 'printer'
)