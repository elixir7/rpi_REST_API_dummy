from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs
from printers import printers
from clint.textui import puts, colored
import time

class History(Resource):
    #__init__ needs to run before get is called or this won't work
    def __init__(self):
        self._lastTime = time.time()

    def get(self):
        currentTime = time.time()
        if(currentTime - self._lastTime > 10):
            self._timer = time
            puts(colored.cyan("Getting printer history from all printers, this will take a while!"))
            historyList = list()
            for printer in printers:
                history = printer.get("/api/v1/history").json()
                historyList.append(history)
                self._historyList = historyList
        #Only do a new request if there has atleast been 10s since last req.
        #Otherwise just return the preious response
        return jsonify(self._historyList)

history_api = Blueprint('resource.history', __name__)
api = Api(history_api)

api.add_resource(
    History,
    '/api/v1/history',
    endpoint = 'history'
)