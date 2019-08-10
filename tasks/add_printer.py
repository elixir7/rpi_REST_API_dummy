from clint.textui import puts, indent, colored, prompt
from tasks.helpers import verticalLine
from printer import Printer
from printers import printerList

import json
import ipaddress

def addPrinter():
    """ Procedure for adding a non existing printer by it's ip adress and writing down key infromation to printers.json
    """
    verticalLine()
    puts(colored.magenta("Add a printer"))
    puts("Find the ip adress by clicking on System > Network on the machine")

    tries = 0
    while tries < 3:
        ip_input = prompt.query("What is the ip adress of the printer? e.g \"192.168.1.201\"")
        try:
            ip = ipaddress.ip_address(ip_input)  
            ip = str(ip)

            #If a connection to the entered IP already exists, stop
            if(duplicateIP(ip)):
                return
            try:
                new_printer = Printer(ip)
                puts(colored.green("Successfully added a new printer"))
                
                #Print out the data
                puts(colored.cyan(new_printer.getName()))
                with indent(4):
                    puts("IP: " + new_printer.getIp())
                    puts("ID: " + new_printer.getId())
                    puts("Key: " + new_printer.getKey())

                #Save back to the file by reading, adding and writing.
                printers = json.load(open("printers.json", "rt"))
                printers.append(new_printer.getPrinterAsDict())
                json.dump(printers, open("printers.json", "w"), indent=4)

                #Update printerList
                printerList.update()
                
                break
            except RuntimeError as e:
                puts(colored.red(str(e)))
                with indent(4): 
                    puts(colored.yellow("Someone probably clicked \"deny\" on the printer, try again."))
            
        except ValueError:
            puts(colored.yellow("You entered an invalid ip adress, try again. (Format: IPv4Address)"))
            tries += 1
    if(tries >= 3):
        puts(colored.red("3 tries of failing is enough, find the ip adress of the printer before attempting again."))

def duplicateIP(ip):
    """Used for detecting if a printer on the given ip adress already exists.
    
    Arguments:
        ip {string} -- [description]
    
    Returns:
        bool -- True if there exists a printer on the given ip adress, otherwise False
    """

    for printer in printerList.getPrinters():
        if(printer["ip"] == ip):
            puts(colored.red("Printer at ip-address <" + ip + "> already exists. Remove it before adding a new connection."))
            return True
    return False


    
