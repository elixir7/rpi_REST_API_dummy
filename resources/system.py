from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs
from printers import printerList
from clint.textui import puts, colored

class System(Resource):
    def get(self):
        puts(colored.cyan("Getting system information from printers"))
        systemInfoList = list()
        for printer in printerList.getPrinters():
            r = printer.get("/api/v1/system")
            if r.status_code == 200:
                systemInfo = r.json()
                systemInfoList.append(systemInfo)
                
        return jsonify(systemInfoList)

system_api = Blueprint('resource.system', __name__)
api = Api(system_api)

api.add_resource(
    System,
    '/api/v1/system',
    endpoint = 'system'
)