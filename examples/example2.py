from ultimaker3 import Ultimaker3
import time

#Used for taking user inut in commandline
import sys


api = Ultimaker3("192.168.1.201", "Example 2 Test")
api.loadAuth("auth.data")

class leds:
    brightness = 100.0
    saturation = 100.0
    hue = 0.0

leds = leds()

# Get all the system data
system = api.get("api/v1/system").json()
print("Printer name " + system["name"])

status = api.get("/api/v1/printer/status").json()
state = api.get("/api/v1/printer/led").json()

leds.brightness = 100
leds.hue = 0
leds.saturation = 100
while True:
    cmdInput = input("Enter hue (0-360): ")
    try:
        hue = int(cmdInput)
        print("Setting hue to: " + cmdInput)
        leds.hue = cmdInput
        api.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": leds.saturation, "hue": leds.hue})
    except ValueError:
        print("Hue must be a number between 0 and 360, try again.")
    

    
    



'''
while True: 
    status = api.get("/api/v1/printer/status").json()
    print(status)
    if status == "idle":
        #Blue
        leds.hue = 240
    elif status == "error":
        #Red
        leds.hue = 0
    elif status == "printing":
        #Yellow
        leds.hue = 50
    elif status == "maintenance":
        #Orange
        leds.hue = 20
    elif status == "booting":
        #Green
        leds.hue = 240
    else:
        #Purple - Something very wrong has happend
        leds.hue = (leds.hue + 10) % 360
    api.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": leds.saturation, "hue": leds.hue})
    time.sleep(1)
'''