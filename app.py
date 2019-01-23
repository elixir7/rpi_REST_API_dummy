#Thoughts

#The endpoints should have a two different responses
#If no parameters is supplied in the url, all the statuses of the printers will be returned in an list
#If a parameter (which printer) is supplied, only that printer data should be returned

#if there are alot of people are requesting we can't request the ultimaker every single time. 
#There needs to be a buffer or timer which prevets in from sending requests.
# E.g a 10s delay on each endpoint

from flask import Flask, render_template

from resources.printer import printer_api
from resources.history import history_api
from resources.system import system_api
from resources.print_job import print_job_api
from resources.camera import camera_api
from resources.esp8266 import esp8266_api

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(printer_api)
app.register_blueprint(history_api)
app.register_blueprint(system_api)
app.register_blueprint(print_job_api)
app.register_blueprint(camera_api)
app.register_blueprint(esp8266_api)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/info')
def into():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
