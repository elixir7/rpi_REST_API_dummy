import requests
import json
import time
from clint.textui import puts, indent, colored, prompt
from getpass import getuser

class Printer:

    #When creating a instance, data must be a legit ip or a dict with the info of the printer
    def __init__(self, data):
        """ Create a printer object
            
        
        Arguments:
            data {string or dict} -- Let the type of data decide what to do. String => Setup a new printer with auth. Dict => Authenticate and connect using id and key.
        """
        if(isinstance(data, str)):
            puts(colored.cyan("Created Printer, will now try to connect..."))
            puts(colored.cyan("Go over to the printer and click allow!"))
            self._ip = data
            self._application = "CASE-RPI Printer Request"
            self._session = requests.Session()
            self._setAuthData("", "")

            self._checkAuth()

            response = self.get("api/v1/system/name")
            self._name = response.json()

        elif(isinstance(data, dict)):        
            self._ip = data["ip"]
            self._name = data["name"]
            self._session = requests.Session()
            self._setAuthData(data["id"], data["key"])

            
            if(not self._checkAuth()):
                puts("Check Auth failed when trying to create printer from dict data")
                return

            puts("Connected to printer - " + colored.cyan(data["name"]))   

            response = self.get("api/v1/system/name")
            self._name = response.json()

    def _setAuthData(self, id, key):
        self._auth_id = id
        self._auth_key = key
        self._auth = requests.auth.HTTPDigestAuth(self._auth_id, self._auth_key)

    def _checkAuth(self):
        """ Verifies that the printer object is valid and authenticated by checking that id exists and that a request and response is successful.
        
        Raises:
            RuntimeError: If the authorization is unautorized.
        
        Returns:
            bool -- True if the authentification was valid, othervise false.
        """
        if self._auth_id == "" or self.get("api/v1/auth/verify").status_code != 200:
            puts(colored.yellow("No authentification ID or auth check failed"))
            puts("Requesting new authentification ID and KEY")
            r = self.post("api/v1/auth/request", data={"application": self._application, "user": getuser()})

            data = response.json()
            self._setAuthData(data["id"], data["key"])


            puts("Trying to get authenticated by the printer, you have 60s to press ACCEPT on the printer")
            while tries <= 60:
                puts(colored.cyan("Waiting for authorization from printer..."))
                response = self.get("api/v1/auth/check/%s" % (self._auth_id))
                data = response.json()

                with indent(4):
                    puts("Message: " + data["message"])
                if data["message"] == "authorized":
                    puts(colored.green("Authorized."))
                    return True
                if data["message"] == "unauthorized":
                    raise RuntimeError("Authorization denied")

                tries++
                time.sleep(1)
            # No accepted authentification from the printer after 60s
            return False    
        return True

    def getName(self):
        return self._name

    def getIp(self):
        return self._ip

    def getId(self):
        return self._auth_id

    def getKey(self):
        return self._auth_key
    
    def getPrinterAsDict(self):
        """ Used for saving down to a file
        
        Returns:
            dict -- A dict containing name, ip, id and key.
        """
        printer = {
            "name": self._name,
            "ip": self._ip,
            "id": self._auth_id,
            "key": self._auth_key
        }
        return printer

    def request(self, method, path, **kwargs):
        """ Send a request (get, put, post) to the printer for e.g chaning the lightning or getting printer status.
        
        Arguments:
            method {string} -- What type of request ("get", "put", "post")
            path {string} -- Path for request, the part after http://IP/ e.g. "api/v1/printer/led"

        Returns:
            Response Object -- Returns a Response object containing the returned information and the originall Request object.
        """

        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
            if "headers" not in kwargs:
                kwargs["headers"] = {"Content-type": "application/json"}


        # What should happen if an exception was raised and what should be returned?????
        # Timeout could perhaps make a authentification request fail because you don't press "accept" on the ultimaker within 7s
        try:
            # Attempt to make a request, raise a Timeout Exception if it takes to long and a HTTP error if the response code is 4XX or 5XX.
            r = self._session.request(method, "http://%s/%s" % (self._ip, path), auth=self._auth, timeout=7.0,  **kwargs).raise_for_status()
        except requests.exceptions.HTTPError as err:
            puts(colored.red("Http Error:" + err))
            return
        except requests.exceptions.ConnectionError as err:
            puts(colored.red("Error Connecting:" + err))
            return
        except requests.exceptions.Timeout as err:
            puts(colored.red("Timeout Error:" + err))
            return
        except requests.exceptions.RequestException as err:
            puts(colored.red("Request Error:" + err))
            return
        return r

    def get(self, path, **kwargs):
        """ Shorthand function to do a "GET" request.
        
        Arguments:
            path {string} -- Path for request, the part after http://IP/ e.g. "api/v1/printer/led"
        
        Returns:
             Response Object -- Returns a Response object containing the returned information and the originall Request object.
        """
        return self.request("get", path, **kwargs)

    def put(self, path, **kwargs):
        """ Shorthand function to do a "PUT" request.
        
        Arguments:
            path {string} -- Path for request, the part after http://IP/ e.g. "api/v1/printer/led"
        
        Returns:
             Response Object -- Returns a Response object containing the returned information and the originall Request object.
        """
        return self.request("put", path, **kwargs)

    def post(self, path, **kwargs):
        """ Shorthand function to do a "POST" request.
        
        Arguments:
            path {string} -- Path for request, the part after http://IP/ e.g. "api/v1/printer/led"
        
        Returns:
             Response Object -- Returns a Response object containing the returned information and the originall Request object.
        """
        return self.request("post", path, **kwargs)