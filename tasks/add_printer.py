from clint.textui import puts, indent, colored, prompt
from tasks.helpers import verticalLine
from printer import Printer

import json
import ipaddress

def addPrinter():
    verticalLine()
    #This has no protection against not ok inputs, needs to be added
    puts(colored.magenta("Add a printer"))
    puts("Find the ip adress by clicking on System > Network on the machine")

    tries = 0
    while tries < 3:
        ip_input = prompt.query("What is the ip adress of the printer? e.g \"192.168.1.201\"")
        try:
            ip = ipaddress.ip_address(ip_input)  
            ip = str(ip)

            printers = json.load(open("printers.json", "rt"))

            #If a connection to the entered IP already exists, stop
            if(duplicateIP(ip,printers)):
                return
            try:
                new_printer = Printer(ip)
                printers.append(new_printer.getPrinterAsDict())
                puts(colored.green("Successfully added a new printer"))
                
                #Print out the dat
                puts(colored.cyan(new_printer.getName()))
                with indent(4):
                    puts("IP: " + new_printer.getIp())
                    puts("ID: " + new_printer.getId())
                    puts("Key: " + new_printer.getKey())

                #Save back to the file
                json.dump(printers, open("printers.json", "w"), indent=4)
                break
            except RuntimeError:
                puts(colored.red("Authorization denied by printer."))
                with indent(4): 
                    puts("Someone probably clicked \"deny\" on the printer, try again.")
            
        except ValueError:
            puts(colored.yellow("You entered an invalid ip adress, try again. (Format: IPv4Address)"))
            tries += 1
    if(tries == 3):
        puts(colored.red("3 tries of failing is enough, find the ip adress of the printer before attempting again."))





def duplicateIP(ip, printers):
    for printer in printers:
        if(printer["ip"] == ip):
            puts(colored.red("Printer at ip-address <" + ip + "> already exists. Remove it before adding a new connection."))
            return True
    return False


    
