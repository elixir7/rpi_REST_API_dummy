from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from machine import machine

class PrintJob(Resource):
    def get(self):
        print_job = machine.get("/api/v1/print_job").json()
        return jsonify(print_job)


print_job_api = Blueprint('resource.print_job', __name__)
api = Api(print_job_api)
api.add_resource(
    PrintJob,
    '/api/v1/print_job',
    endpoint = 'print_job'
)