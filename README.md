# Ultimaker3 API - CASE LAB
Two main parts.
  - **cmd.py** is a commandline interface which has CRUD (Create, Read, Update+, Delete) actions for setting up the printer farm.
  - **app.py** Runs a webserver with flask on python which is an API for getting useful information out of the printers.

### HEADS UP
This is Über early development, pre alpha. Will not work if you don't know what you are doing.

### Requires
Everything runs on python 3. 
Install the following packages by running the command.
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

### Useful commands
In order to kill a process running on a ceratin port you can use the following commands.
Make suer you got **lsof** installed, if not run "sudo apt install lsof"
List processes running on a port:
"lsof -i:port" => "lsof -i:8080" lists the port on port 8080.

You can then kill them by using:
"kill PID" PID = process ID.
If that doesn't work you can use the flag -9 to force it.
"kill -9 PID" will kill the process.
