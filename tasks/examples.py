from clint.textui import puts, indent, colored, prompt
from tasks.helpers import verticalLine
from printers import printerList

import json
import ipaddress


example_menu = [{'selector':'1', 'prompt':'Change color on all printers', 'return':'ca'},
                {'selector':'2', 'prompt':'Change color on specific printer', 'return':'cs'},
                {'selector':'e', 'prompt':'Go back', 'return':'e'}]

def examples():
    """ Procedure for choosing and running example 
    """
    keep_asking = True
    while keep_asking:
        verticalLine()
        example = prompt.options(colored.magenta("What would you like to try out?"), example_menu)
        if(example == "ca"):
            changeColorAll()
        elif(example == "cs"):
            changeColorSpecific()
        elif (example == "exit"):
            keep_asking = False
        else:
            puts(colored.yellow("Wrong input, try again"))

def changeColor(printer, hue, saturation, brightness):
    """Change color of a specific printer with HSV colors
    
    Arguments:
        printer {Printer} -- Printer to change color on
        hue {str} -- Hue
        saturation {str} -- Saturation
        brightness {str} -- Brightness
    """
    r = printer.get("api/v1/system")
    if(r.status_code != 200):
        return

    systemInfo = r.json()
    if systemInfo['variant'] == "Ultimaker S5":
        #The UM S5 does not have rgb lightning...  and saturation is inverted so only change the brightness
        printer.put("api/v1/printer/led", data={"brightness": brightness, "saturation": 0, "hue": hue})
    else:
        printer.put("api/v1/printer/led", data={"brightness": brightness, "saturation": saturation, "hue": hue})

def getColorData():
    """Asks for hue, saturation and brightness as inputs in the CMD
    
    Returns:
        dict -- If values were ok returns dict containing "hue", "saturation" and "brightness", empty if not.
    """
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

            return  {
                "hue" : hue,
                "saturation" : saturation,
                "brightness" : brightness
            }
        except ValueError:
            puts(colored.yellow("Hue must be a number between 0 and 360, try again."))
            tries += 1
    if(tries >= 3):
        puts(colored.red("3 tries of failing is enough, quitting example"))
    return {}

def changeColorAll():
    """Changes color on all printers
    """
    verticalLine()
    puts(colored.cyan("Example - Change color on all printers"))
    colors = getColorData()

    if not colors: #An empty dict is False
        return

    for printer in printerList.getPrinters():
        changeColor(printer, colors['hue'], colors['saturation'], colors['brightness'])

def changeColorSpecific():
    """Changes color on a specific printer
    """
    verticalLine()
    puts(colored.cyan("Example - Change color on a specific printer"))
    puts("Available printers: ")
    for printer in printerList.getPrinters():
        puts("Name: %s, IP: <%s>" % (printer.getName(), printer.getIp()))

    ip_input = prompt.query("Enter printer ip: ")
    try:
        ip = ipaddress.ip_address(ip_input) 
        ip = str(ip) 

        for printer in printerList.getPrinters():
            if printer.getIp() == ip:
                colors = getColorData()

                if not colors: #An empty dict is False
                    return

                changeColor(printer, colors['hue'], colors['saturation'], colors['brightness'])
    except ValueError:
        puts(colored.yellow("You entered an invalid ip adress. (Format: IPv4Address)"))


