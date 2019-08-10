import json

from printer import Printer
from clint.textui import puts, colored


class PrinterList:

    def __init__(self):
        self.update()

    """ Update current printer list with info in the printers.json file. 
        Use this function when a printer which has been offline goes online to add it back and vise versa.
        Used in constructor for setting up initial list.
    """
    def update(self):
        json_file = json.load(open("printers.json", "rt"))
        self._printers = list()

        for printer_data in json_file:
            try:
                new_printer = Printer(printer_data)
                self._printers.append(new_printer)
            except RuntimeError:
                puts(colored.red("Could not add printer at ip: %s" % printer_data['ip']))
    
                
    def getPrinters(self):
        """Return a list of authenticated printers.
        
        Returns:
            list -- Authenticated printers.
        """
        return self._printers


 
 
 