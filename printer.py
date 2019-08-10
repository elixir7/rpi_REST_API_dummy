import requests
import json
import time
from clint.textui import puts, indent, colored, prompt
from getpass import getuser

class Printer:

    def __init__(self, data):
        """ Create a printer object
            
        Raises:
            RuntimeError: If authentification check is not passed, the printer object can't be created.
        
        Arguments:
            data {string or dict} -- Let the type of data decide what to do. String => Setup a new printer with auth. Dict from json data => Authenticate and connect using id and key.
        """

        if isinstance(data, str):
            self._ip = data
            self._application = "CASE LAB - RPI Printer Request"
            self._session = requests.Session()
            self._setAuthData("", "")

            puts(colored.cyan("Trying to connect to printer on ip: " + data))

            if self._checkAuth():
                response = self.get("api/v1/system/name")
                self._name = response.json()
            else:
                raise RuntimeError("Authentification check failed when trying to create printer from string data (ip adress): %s" % self._ip)
                

        elif isinstance(data, dict):        
            self._ip = data["ip"]
            self._name = data["name"]
            self._session = requests.Session()
            self._setAuthData(data["id"], data["key"])

            
            if not self._checkAuth():
                raise RuntimeError("Authentification check failed when trying to create printer from dict data")

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
            RuntimeError: If the authorization failed
        
        Returns:
            bool -- True if the authentification was valid, otherwise false.
        """

        if self._auth_id == "" or self.get("api/v1/auth/verify").status_code != 200:
            puts(colored.yellow("No authentification ID or auth. check failed"))
            puts("Requesting new authentification ID and KEY")
            r = self.post("api/v1/auth/request", data={"application": self._application, "user": getuser()})

            if(r.status_code != 200):
                return False

            data = r.json()
            self._setAuthData(data["id"], data["key"])

            puts("Recieved ID and KEY")
            puts("Trying to get authenticated by the printer, you have 60s to press ACCEPT on the printer")
            
            tries = 0
            while tries <= 60:

                if(tries % 10 == 0):
                    puts("Waiting for authorization from printer...")
                
                response = self.get("api/v1/auth/check/%s" % (self._auth_id))
                data = response.json()

                with indent(4):
                    puts("Message: " + data["message"])
                if data["message"] == "authorized":
                    puts(colored.green("Authorized."))
                    return True
                if data["message"] == "unauthorized":
                    puts(colored.red("Unauthorized."))
                    return False

                tries += 1
                time.sleep(1)
                
            # No accepted authentification from the printer after 60s
            return False    
        # Auth_ID exsisted and was verified by the printer.
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
        except requests.exceptions.ConnectionError as err:
            puts(colored.red("Error Connecting:" + err))
        except requests.exceptions.Timeout as err:
            puts(colored.red("Timeout Error:" + err))
        except requests.exceptions.RequestException as err:
            puts(colored.red("Request Error:" + err))
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