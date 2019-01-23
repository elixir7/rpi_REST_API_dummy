# Ultimaker3 API - CASE LAB
Two main parts. 
    - **cmd.py** is a commandline interface which has CRUD (Create, Read, Update+, Delete) actions for setting up the printer farm.
    - **app.py** Runs a webserver with flask on python which is an API for getting useful information out of the printers.

### HEADS UP
This is Über early development, pre alpha. Will not work if you don't know what you are doing.

### Requires
Everything runs on python 3. 
Install the following command to install dependencies.
```sh
$ pip3 install package-name
```
    - **clint**
    - **werkzeug**
    - **flask**
    - **flask-restful**

### Running the program
In order to set up the machines and the server you must first configure via the CMD.
Open up the terminal and change directory to this project, then run.
```sh
$ python3 cmd.py
```
Follow the steps until all machines are set up, then you can exit that application.

Then start the statuschecker in a separate shell (keep it running) by running:
```sh
$ python3 status_checker.py
```

Then you can start the server in a separate shell (keep it running) by running (runs in debug mode on http://0.0.0.0:8000):
```sh
$ python3 app.py
```

### TODO
If not all printers are connected to the network the system will not work since the program will try to send requests to an IP that has no reciever. This needs to be fixed ASAP.

### Ultimaker 3  JSON Data
This is just used for writing down data that will be needed later.
{
    "name": "CASE-Lab-UM3",
    "ip": "192.168.1.201",
    "id": "e4a69cf7286b414e1f85206851fecb93",
    "key": "38cd2e19fce0533e3f66c5dae1df84bdbea0a1d9c2779cb5118dd3be55f2c186"
},
{
    "name": "CASE-Lab-UMS5",
    "ip": "192.168.1.242",
    "id": "b8bad80c28abe2812342285d08a20d08",
    "key": "db0190c07220cd7927b9403c21c14a4b00b1a4f60332ebb7de632e8d4d1594c4"
}
