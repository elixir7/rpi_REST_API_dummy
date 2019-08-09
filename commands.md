#Useful commands
In order to kill a process running on a ceratin port you can use the following commands.
Make suer you got **lsof** installed, if not run "sudo apt install lsof"
List processes running on a port:
"lsof -i:port" => "lsof -i:8080" lists the port on port 8080.

You can then kill them by using:
"kill PID" PID = process ID.
If that doesn't work you can use the flag -9 to force it.
"kill -9 PID" will kill the process.
