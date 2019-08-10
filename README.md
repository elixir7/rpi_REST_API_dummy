# Ultimaker3 API - CASE LAB
Three main parts.
  - **cmd.py** is a commandline interface which has Add, Read, Update(not implemented), Remove actions for setting up the printer farm with authentification.
  - **app.py** Runs a webserver with flask on python which acts as an API for getting information out of the printers and sending html/css files to the user.
  - **status_checker.py** Runs a loop which checks states on printers (running, idle, error) and changes colors accordingly. This is not dependant on app.py to run.

### HEADS UP
This is early development. Will probably not work if you don't know what you are doing.

### Requirements
Everything runs on Python 3 with a couple packages. 
Install the following packages by running the command.
```sh
$ pip3 install package-name
```
  - **requests** HTTP-requests for humans
  - **clint** Command Line Interface 
  - **werkzeug** Chaching information
  - **flask**  Web application framework for python   
  - **flask-restful** Extension to flask for building REST-APIs

### Running the program
In order to set up the printers and the server you must first run the configuration via the cmd (command line/terminal).
Open up the terminal and change directory to this project, then run.
```sh
$ python3 cmd.py
```
Follow the steps (Add printer) until all machines are set up, then you can exit that application.

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
