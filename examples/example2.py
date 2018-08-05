from ultimaker3 import Ultimaker3
import time

api = Ultimaker3("192.168.100.110", "Test script")
api.loadAuth("auth.data")

# Get all the system data
system = api.get("api/v1/system").json()
print(system["name"])

status = api.get("/api/v1/printer/status").json()
print(status)

class leds:
    brightness = 100.0
    saturation = 360.0
    hue = 0.0

leds = leds()


while 1: 
    print(status)
    if status == "idle":
        #Green
        leds.hue = 110
    elif status == "error":
        #Red
        leds.hue = 0
    #elif status == "printing":
        #Yellow
        leds.hue = 50
    elif status == "maintenance":
        #Orange
        leds.hue = 20
    elif status == "booting":
        #Blue
        leds.hue = 240
    else:
        #Purple
        leds.hue = (leds.hue + 10) % 360
    api.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": leds.saturation, "hue": leds.hue})
    time.sleep(0.01)


