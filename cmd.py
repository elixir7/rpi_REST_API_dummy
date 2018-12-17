from __future__ import print_function
from clint.textui import puts, indent, colored, validators, prompt

import sys
import os
import time
import json

from ultimaker import Ultimaker
from tasks.helpers import verticalLine, showPrinters
from tasks.add_printer import addPrinter
from tasks.examples import examples
from tasks.remove_printer import removePrinter

sys.path.insert(0, os.path.abspath('..'))

#Needs to be extracted to separate files
def updatePrinters():
    puts("Update printers is not implemented")
    puts(colored.cyan("Remove printer and add a new one to update."))
def wrong_input():
    puts(colored.red("Wrong input, try again"))


main_menu = [{'selector':'e','prompt':'Examples','return':'e'},
                {'selector':'s','prompt':'Show printers','return':'s'},
                {'selector':'a','prompt':'Add printer','return':'a'},
                {'selector':'r','prompt':'Remove printer','return':'r'},
                {'selector':'u','prompt':'Update printer','return':'u'},
                {'selector':'exit','prompt':'Exit program','return':'exit'}]

while True:
    verticalLine()
    action = prompt.options(colored.magenta("What would you like to do?"), main_menu)
    if(action == "e"):
        examples()
    elif(action == "s"):
        showPrinters()
    elif(action == "a"):
        addPrinter()
    elif(action == "r"):
        removePrinter()
    elif(action == "u"):
        updatePrinters()
    elif(action == "exit"):
        exit()
    else:
        wrong_input


