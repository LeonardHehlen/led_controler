import serial
import time

class ArduinoCommunication(object):

    def __init__(self, port, baudrate, timeout,msg):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.msg = msg

        self.s = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    
    def send(self):
        self.msg = str.encode(self.msg + '\n')
        print("Message Sent: ", self.msg)
        
        def com(self):
            s = self.s
            r = s.read()
            while r == b'':
                time.sleep(0.05)
                r = s.read(size=64)
                nr = r.decode("utf-8")
                s.write(self.msg)

            s.write(str.encode(""))
            nr = nr.split("\n")
            nr = nr[0]
            print(nr)
        com(self)