from clint.textui import puts, indent, colored
from printers import printerList
import json

def verticalLine():
    puts("-----------------------------------------------------------------------------")

def showPrinters():
    verticalLine()
    puts(colored.magenta("Printers"))
    sortedPrinters = sorted(printerList.getPrinters(), key=lambda k: k["name"])

    for printer in sortedPrinters:
        puts(colored.cyan(printer["name"]))
        with indent(4):
            puts("IP-address: " + printer["ip"])
            puts("ID: " + printer["id"])
            puts("Key: " + printer["key"])