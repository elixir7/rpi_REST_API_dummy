from clint.textui import puts, indent, colored
from printers import printerList
import json

def verticalLine():
    puts("-----------------------------------------------------------------------------")

def showPrinters():
    """Prints a vetical line followed by all printers and all their info.
    """
    verticalLine()
    puts(colored.magenta("Printers"))
    sortedPrinters = sorted(printerList.getPrinters(), key=lambda k: k.getName())

    for printer in sortedPrinters:
        puts(colored.cyan(printer.getName()))
        with indent(4):
            puts("IP-address: " + printer.getIp())
            puts("ID: " + printer.getId())
            puts("Key: " + printer.getKey())

def showPrintersBasic():
    """Prints printer name and ip on one line each
    """
    sortedPrinters = sorted(printerList.getPrinters(), key=lambda k: k.getName())
    for printer in sortedPrinters:
        puts("%s\t%s" % (printer.getName(), printer.getIp()))

