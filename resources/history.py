from flask import jsonify, Blueprint
from flask_restful import Resource, Api
from printers import printerList
from clint.textui import puts, colored
from werkzeug.contrib.cache import SimpleCache


#By using cache we can speed up the server by a ton!
#Getting all printer history from the printers is time consuming and should not be done too often.
#In this case we update it when a user requests it and if it hasn't been updated for 30min.
cache = SimpleCache()


class History(Resource):
    def get(self):
        history = cache.get("history")
        if history is None:
            puts(colored.cyan("Getting new printer history from all printers, this will take a while!"))
            historyList = list()
            for printer in printerList.getPrinters():
                r = printer.get("/api/v1/history")
                if r.status_code == 200:
                    data = r.json()
                    historyList.append(data)

            #Remove the cache after 30min.
            cache.set("history", historyList, timeout=30*60)
            history = cache.get("history")
        
        return jsonify(history)
    
history_api = Blueprint('resource.history', __name__)
api = Api(history_api)

api.add_resource(
    History,
    '/api/v1/history',
    endpoint = 'history'
)