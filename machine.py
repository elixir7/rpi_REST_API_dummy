from ultimaker3 import Ultimaker3

ip = '192.168.1.201'
instance = 'Test Script'

machine = Ultimaker3(ip, instance)
machine.loadAuth("auth.data")


