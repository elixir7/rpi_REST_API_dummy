from printer import Printer
from clint.textui import puts, indent, colored

import json
import time

#HSV colors, think of a cirle, 360deg.
red = 0
yellow = 50
orange = 20
blue = 200
green = 240
purple = 283

class Leds:
    brightness = 100.0
    saturation = 100.0
    hue = 240
leds = Leds()



puts("-----------------------------------------------------------------------------")
puts(colored.magenta("Status Checker running"))

json = json.load(open("printers.json", "rt"))

printers = list()

for json_printer in json:
    printer = Printer(json_printer)
    printers.append(printer)

while True:
    puts("-----------------------------------------------------------------------------")
    time.sleep(5)
    for printer in printers:
        status = printer.get("/api/v1/printer/status").json()
        if status == "idle":
            leds.hue = blue
            puts(printer.getName() + " - " + colored.cyan(status))
        elif status == "error":
            leds.hue = red
            puts(printer.getName() + " - " + colored.red(status))
        elif status == "printing":
            leds.hue = yellow
            puts(printer.getName() + " - " + colored.yellow(status))
        elif status == "maintenance":
            leds.hue = orange
            puts(printer.getName() + " - " + status)
        elif status == "booting":
            leds.hue = green
            puts(printer.getName() + " - " + colored.green(status))
        else:
            leds.hue = purple
            puts(printer.getName() + " - " + status)

        if "UMS5" in printer.getName():
            #UMS5 has inverted saturation for some reason
            printer.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": 0, "hue": leds.hue})
        else:
            printer.put("api/v1/printer/led", data={"brightness": leds.brightness, "saturation": 100.0, "hue": leds.hue})
