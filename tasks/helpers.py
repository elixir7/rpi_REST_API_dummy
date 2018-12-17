from clint.textui import puts, indent, colored
import json

def verticalLine():
    puts("-----------------------------------------------------------------------------")

def showPrinters():
    verticalLine()
    puts(colored.magenta("Printers"))
    printers = json.load(open("printers.json", "rt"))
    sortedPrinters = sorted(printers, key=lambda k: k["name"])

    for printer in sortedPrinters:
        puts(colored.cyan(printer["name"]))
        with indent(4):
            puts("IP-address: " + printer["ip"])
            puts("ID: " + printer["id"])
            puts("Key: " + printer["key"])