from clint.textui import puts, indent, colored, prompt
from tasks.helpers import verticalLine
from printer import Printer

import json


example_menu = [{'selector':'1', 'prompt':'Change color', 'return':'c'},
                {'selector':'e', 'prompt':'Go back', 'return':'e'}]

def examples():
    keep_asking = True
    while keep_asking:
        verticalLine()
        example = prompt.options(colored.magenta("What would you like to try out?"), example_menu)
        if(example == "c"):
            changeColor()
        elif (example == "e"):
            keep_asking = False
        else: 
            puts("This should not be happening")

def changeColor():
    verticalLine()
    puts(colored.cyan("Example - Change color"))
    tries = 0
    while tries < 3:
        hue_input = prompt.query("Enter hue (0-360): ")
        sat_input = prompt.query("Enter saturation (0-100): ")
        brightness_input = prompt.query("Enter brightness (0-100): ")
        try:
            hue = int(hue_input)
            saturation = int(sat_input)
            brightness = int(brightness_input)

            puts("Setting hue: " + str(hue) + ", saturation: " + str(saturation) + ", brightness: " + str(brightness))

            printers_json = json.load(open("printers.json", "rt"))
            printers = list()

            for printer_json in printers_json:
                printer = Printer(printer_json)
                printers.append(printer)
            
            for printer in printers:
                systemInfo = printer.get("api/v1/system").json()
                if systemInfo['variant'] == "Ultimaker S5":
                    #The UM S5 does not have rgb lightning...  and saturation is inverted so only change the brightness
                    printer.put("api/v1/printer/led", data={"brightness": brightness, "saturation": 0, "hue": hue})
                else:
                    printer.put("api/v1/printer/led", data={"brightness": brightness, "saturation": saturation, "hue": hue})
                #if "UMS5" in printer.getName():
                    #UMS5 has inverted saturation for some reason
                #    printer.put("api/v1/printer/led", data={"brightness": 100.0, "saturation": 0, "hue": hue})
                #else:
                #    printer.put("api/v1/printer/led", data={"brightness": 100.0, "saturation": 100.0, "hue": hue})
                
            break
        except ValueError:
            puts(colored.yellow("Hue must be a number between 0 and 360, try again."))
            tries += 1
    if(tries >= 3):
        puts(colored.red("3 tries of failing is enough, quitting example"))