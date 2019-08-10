from clint.textui import puts, indent, colored
from tasks.helpers import verticalLine
from printers import printerList
from colors import *
import json
import time

class Led:
    #HSV color
    brightness = 100.0,
    saturation = 100.0
    hue = 240
    
    #RGB color (0-1023)
    r = 0
    g = 0
    b = 0
    

#Create a LED object
led = Led()

verticalLine()
puts(colored.magenta("Status Checker running"))

while True:
    verticalLine()
    espData = json.load(open("esp8266_data.json", "rt"))

    if len(espData) != len(printerList.getPrinters()):
        new_esp_list = list()
        for i, printer in printerList.getPrinters():
            esp_device = {
                "MODULE_ID": i,
                "R_Value": 0, 
                "G_Value": 0,       
                "B_Value": 0,
                "FAN_ON": False
            }
            new_esp_list.append(esp_device)
        espData = new_esp_list

    for i, printer in printerList.getPrinters():

        r = printer.get("/api/v1/printer/status")
        if(r.status_code != 200):
            #Skip the printer if we don't get a good response
            continue

        status = r.json()
        puts(printer.getName() + " - " + status)
        if status == "idle":
            led.hue = green
            led.r = rGreen
            led.g = gGreen
            led.b = bGreen
        elif status == "error":
            led.hue = red
            led.r = rRed
            led.g = gRed
            led.b = bRed
        elif status == "printing":
            led.hue = blue
            led.r = rBlue
            led.g = gBlue
            led.b = bBlue

            #Turn on the fan
            espData[i]["FAN_ON"] = True
        elif status == "maintenance":
            led.hue = orange
            led.r = rOrange
            led.g = gOrange
            led.b = bOrange
        else:
            led.hue = purple
            led.r = rPurple
            led.g = gPurple
            led.b = bPurple
        
        if status != "printing":
            espData[i]["FAN_ON"] = False

        r = printer.get("api/v1/system")
        if(r.status_code != 200): 
            #If the response is bad we skip that printer
            continue
        else:
            systemInfo = r.json()
            if systemInfo['variant'] == "Ultimaker S5":
                #The UM S5 does not have rgb lightning, and saturation is inverted
                #We adjust brightness on the printer if needed and send data to the esp8266 to turn on our own RGB led.
                printer.put("api/v1/printer/led", data={"brightness": led.brightness, "saturation": 0, "hue": 0})
                espData[i]["R_Value"] = led.r
                espData[i]["G_Value"] = led.g
                espData[i]["B_Value"] = led.b
            else:
                #On a Ultimaker 3/3 Extended we update the built in led.
                printer.put("api/v1/printer/led", data={"brightness": led.brightness, "saturation": led.saturation, "hue": led.hue})

        #Save the json data back to the file.
        json.dump(espData, open("esp8266_data.json", "w"), indent=4)

    # Take a break in between every check round.        
    time.sleep(5)
        

