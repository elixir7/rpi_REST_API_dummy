from printer import Printer
import json

json = json.load(open("printers.json", "rt"))
printers = list()

for json_data in json:
    new_printer = Printer(json_data)
    printers.append(new_printer)

