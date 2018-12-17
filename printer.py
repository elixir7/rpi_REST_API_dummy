import requests
import json
import time
from clint.textui import puts, indent, colored, prompt
from getpass import getuser

#####       _ = private method

class Printer:

    #When creating a instance, data must be a legit ip or a dict with the info of the printer
    def __init__(self, data):
        #Let the type of data decide what to do. 
        if(isinstance(data, str)):
            puts(colored.cyan("Created Printer, will now try to connect..."))
            puts(colored.cyan("Go over to the printer and click allow!"))
            self._ip = data
            self._application = "CASE-RPI Printer Request"
            self._session = requests.sessions.Session()
            self._setAuthData("", "")

            self._checkAuth()

            response = self.get("api/v1/system/name")
            self._name = response.json()

        elif(isinstance(data, dict)): 
            puts("Connected to printer - " + colored.cyan(data["name"]))        
            self._ip = data["ip"]
            self._name = data["name"]
            self._session = requests.sessions.Session()
            self._setAuthData(data["id"], data["key"])

            self._checkAuth()

            response = self.get("api/v1/system/name")
            self._name = response.json()

    def _setAuthData(self, id, key):
        self._auth_id = id
        self._auth_key = key
        self._auth = requests.auth.HTTPDigestAuth(self._auth_id, self._auth_key)

    def _checkAuth(self):
        if self._auth_id == "" or self.get("api/v1/auth/verify").status_code != 200:
            puts(colored.yellow("No auth or auth check failed, requesting new authentication"))
            response = self.post("api/v1/auth/request", data={"application": self._application, "user": getuser()})
            if response.status_code != 200:
                puts(colored.red("Failed to request new API key"))
                raise RuntimeError("Failed to request new API key")
            data = response.json()
            self._setAuthData(data["id"], data["key"])
            while True:
                time.sleep(1)
                response = self.get("api/v1/auth/check/%s" % (self._auth_id))
                data = response.json()
                puts("Waiting for authorization from printer...")
                with indent(4):
                    puts("Message: " + data["message"])
                if data["message"] == "authorized":
                    puts(colored.green("Authorized."))
                    return True
                if data["message"] == "unauthorized":
                    raise RuntimeError("Authorization denied")
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
    
    #Used for saving down to a file
    def getPrinterAsDict(self):
        printer = {
            "name": self._name,
            "ip": self._ip,
            "id": self._auth_id,
            "key": self._auth_key
        }
        return printer

    # Do a new HTTP request to the printer. It formats data as JSON, and fills in the IP part of the URL.
    def request(self, method, path, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
            if "headers" not in kwargs:
                kwargs["headers"] = {"Content-type": "application/json"}
        return self._session.request(method, "http://%s/%s" % (self._ip, path), auth=self._auth, **kwargs)

    # Shorthand function to do a "GET" request.
    def get(self, path, **kwargs):
        return self.request("get", path, **kwargs)

    # Shorthand function to do a "PUT" request.
    def put(self, path, **kwargs):
        return self.request("put", path, **kwargs)

    # Shorthand function to do a "POST" request.
    def post(self, path, **kwargs):
        return self.request("post", path, **kwargs)