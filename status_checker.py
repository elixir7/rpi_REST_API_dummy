from clint.textui import puts, indent, colored
from printers import printers
import json
import time

#HSV colors, think of a cirle, 360deg.
#RGB 0-255 converted to 0-1023
#Move this to a separate file please
CR = 1023/255 #Convertion ratio for 0-1023 RGB

red = 0
rRed = int(CR*255)
gRed = 0
bRed = 0


yellow = 50
rYellow = int(CR * 255)
gYellow = int(CR * 213)
bYellow = 0

orange = 20
rOrange = int(CR* 255)
gOrange = int(CR*85)
bOrange = 0

blue = 200
rBlue = 0
gBlue = int(CR*170)
bBlue = int(CR*255)

green = 240
rGreen = 0
gGreen = 0
bGreen = int(CR*255)

purple = 283
rPurple = int(CR*183)
gPurple = 0
bPurple = int(CR*255)



class Leds:
    #HSV color
    brightness = 100.0,
    saturation = 100.0
    hue = 240
    
    #RGB color (0-1023)
    r = 0
    g = 0
    b = 0
    
leds = Leds()



puts("-----------------------------------------------------------------------------")
puts(colored.magenta("Status Checker running"))

while True:
    puts("-----------------------------------------------------------------------------")
    time.sleep(5)
    espData = json.load(open("esp8266_data.json", "rt"))
    index = 0
    #This assumes amountOfesp8266 >= amountOfPrinters, if not this will crash.

    for printer in printers:
        espData[index]["MODULE_ID"] = index
        status = printer.get("/api/v1/printer/status").json()
        if status == "idle":
            leds.hue = blue
            leds.r = rBlue
            leds.g = gBlue
            leds.b = bBlue
            puts(printer.getName() + " - " + colored.cyan(status))
        elif status == "error":
            leds.hue = red
            leds.r = rRed
            leds.g = gRed
            leds.b = bRed
            puts(printer.getName() + " - " + colored.red(status))
        elif status == "printing":
            leds.hue = yellow
            leds.r = rYellow
            leds.g = gYellow
            leds.b = bYellow
            puts(printer.getName() + " - " + colored.yellow(status))
            #Turn on the fan
            espData[index]["FAN_ON"] = True
        elif status == "maintenance":
            leds.hue = orange
            leds.r = rOrange
            leds.g = gOrange
            leds.b = bOrange
            puts(printer.getName() + " - " + colored.red(status))
        elif status == "booting":
            leds.hue = green
            leds.r = rGreen
            leds.g = gGreen
            leds.b = bGreen
            puts(printer.getName() + " - " + colored.green(status))
        else:
            leds.hue = purple
            leds.r = rPurple
            leds.g = gPurple
            leds.b = bPurple
            puts(printer.getName() + " - " + status)

        #Turn off fan if it isn't printing
        if status != "printing":
            espData[index]["FAN_ON"] = False

        if "UMS5" in printer.getName():
            #Update the RGB value to the ESP8266 LED STRIP
            espData[index]["R_Value"] = leds.r
            espData[index]["G_Value"] = leds.g
            espData[index]["B_Value"] = leds.b
        else:
            #Send a post request to change the leds on Ultimaker 3 standard and Extended
            printer.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": leds.saturation, "hue": leds.hue})
        index = index + 1

        #Save the json data back to the file.
        json.dump(espData, open("esp8266_data.json", "w"), indent=4)

