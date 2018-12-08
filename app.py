#Pseudo kod

#1. En user skickar en GET request och RPI får in en GET HTTP request på en URL från en dator någonstans som 
# (t.ex ip-adress:8000/api/v1/print_job/time_elapsed) för att kunna visa på sidan för användaren
#2. RPIn förstår requesten och skickar en GET request till UM3 api på det lokala nätverket
#3. När RPIn har fått tillbaka det skickar den tillbaka det till den som förfrågat (user)
#4. Det är sedan upp till script.js att hålla koll värdena den fick tillbaka och göra beräkningar så som att 
#  räkna ner elapsed time.

# Questions
# 1. Ska script köra en main loop som skickar förfrågningar hela tiden?
#       Isåfall kommer ju RPIn överbelastas om massa gör det
# 2. Hur i F** ska man få upp en kamera feed?
#      En route typ /camera/feed som bara skickar tillbaka det som finns på UM3 camera feed
#       Känns dock märkligt, hur fasen samlar RPIn upp det konstant och skickar ut konstant?
from flask import Flask, render_template


from resources.printer import printer_api
from resources.history import history_api
from resources.system import system_api
from resources.print_job import print_job_api
from resources.camera import camera_api



DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(printer_api)
app.register_blueprint(history_api)
app.register_blueprint(system_api)
app.register_blueprint(print_job_api)
app.register_blueprint(camera_api)


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)


