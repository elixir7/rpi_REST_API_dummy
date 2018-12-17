from clint.textui import puts, indent, colored, prompt
from tasks.helpers import verticalLine
from ultimaker import Ultimaker
from printer import Printer

import json
import ipaddress

def removePrinter():
    verticalLine()
    #This has no protection against not ok inputs, needs to be added
    puts(colored.magenta("Remove a printer"))

    printers = json.load(open("printers.json", "rt"))

    puts(colored.cyan("Printers"))
    for printer in printers:
        puts(printer["name"] + " - " + printer["ip"])

    tries = 0
    while tries < 3:
        ip_input = prompt.query("Type the ip adress of the printer you wish to remove: ")
        try:
            ip = ipaddress.ip_address(ip_input)  
            ip = str(ip)

            input =  prompt.query("Are you sure you want to delete printer "  + ip +": <yes/no>")
            if(str(input).upper().lower() == "yes"):
                for printer in printers:
                    if(printer["ip"] == ip):
                        printers.remove(printer)
                        #Save back to the file
                        json.dump(printers, open("printers.json", "w"), indent=4)
                        puts(colored.green("Printer sucessfully removed!"))
                        return
                puts(colored.red("Failed to remove printer, check remove_printer.py file"))
            else:
                puts(colored.red("Write \"yes\" or no please"))
            
        except ValueError:
                puts(colored.yellow("You entered an invalid ip adress, try again. (Format: IPv4Address)"))
                tries += 1

    
