from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from printers import printers
from clint.textui import puts, colored
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

#Gets the current print jobs
class PrintJob(Resource):
    def get(self):
        printJobs = cache.get("printJobs")
        if printJobs is None:
            puts(colored.cyan("Getting current print jobs"))
            printJobList = list()
            for printer in printers:
                printerJob = printer.get("/api/v1/print_job").json()
                printJobList.append(printerJob)
            cache.set("printJobs", printJobList, timeout=5)
            printJobs = cache.get("printJobs")
        return jsonify(printJobs)


print_job_api = Blueprint('resource.print_job', __name__)
api = Api(print_job_api)
api.add_resource(
    PrintJob,
    '/api/v1/print_job',
    endpoint = 'print_job'
)