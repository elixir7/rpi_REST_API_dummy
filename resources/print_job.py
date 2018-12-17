from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from printers import printers
from clint.textui import puts, colored

class PrintJob(Resource):
    def get(self):
        puts(colored.cyan("Getting current print jobs"))
        printJobList = list()
        for printer in printers:
            printerJob = printer.get("/api/v1/print_job").json()
            printJobList.append(printerJob)
        return jsonify(printJobList)


print_job_api = Blueprint('resource.print_job', __name__)
api = Api(print_job_api)
api.add_resource(
    PrintJob,
    '/api/v1/print_job',
    endpoint = 'print_job'
)