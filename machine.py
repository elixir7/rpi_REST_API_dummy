from ultimaker3 import Ultimaker3

ip = '192.168.100.110'
instance = 'Test Script'

machine = Ultimaker3(ip, instance)
machine.loadAuth("auth.data")


