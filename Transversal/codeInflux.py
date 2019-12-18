import time
import argparse
import signal
import sys
import socket
import SocketServer
import serial
import threading
import json
from influxdb import InfluxDBClient

HOST           = "0.0.0.0"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TLH" , "THL" , "LTH" , "LHT" , "HTL" , "HLT"]
FILENAME        = "/home/pi/values.txt"
LAST_VALUE      = ""

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        if data != "":
                        if data in MICRO_COMMANDS: # Send message through UART
                                sendUARTMessage(data)
                                
                        elif data == "getValues()": # Sent last value received from micro-controller
                                print("Sending last values to client")
                                socket.sendto(LAST_VALUE, self.client_address)   
                        else:
                                print("Unknown message: ",data)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


# send serial message 
SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():        
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print('Starting Up Serial Monitor')
        try:
                ser.open()
        except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()


def sendUARTMessage(msg):
    ser.write(msg+'\n\r')
    print("Message <" + msg + "> sent to micro-controller." )


def sendDataToDB(data):
        try:
                client = InfluxDBClient(host="localhost", port=8086, username="miniprojet", password="miniprojet") # Connect to influxDB on localhost
                client.switch_database("miniprojet")
                return client.write_points(data) # write data points
        except:
                print("Couldn't write points to influxDB")
                return False

# Main program logic follows:
if __name__ == '__main__':
        initUART()
        f= open(FILENAME,"a")
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
                server_thread.start()
                print("Server started at {} port {}".format(HOST, UDP_PORT))
                while ser.isOpen() : 
                        time.sleep(2)
                        data_str = ser.readline()
                        f.write(data_str)
                        LAST_VALUE = data_str
                        print("Received : " + data_str)
                        try:
                                data_JSON = json.loads(data_str)
                        except:
                                print("JSON parsing failed")
                                continue
                        else:
                                # Formatting data points for InfluxDB
                                data_influx = [
                                        {
                                                "measurement": "temperature",
                                                "fields": {
                                                        "value": data_JSON["Temp"]
                                                }
                                        },
                                        {
                                                "measurement": "humidity",
                                                "fields": {
                                                        "value": data_JSON["Humidity"]
                                                }
                                        },
                                        {
                                                "measurement": "luminosity",
                                                "fields": {
                                                        "value": data_JSON["Lux"]
                                                }
                                        },
                                ]

                                # Sending measurements to InfluxDB
                                sendDataToDB(data_influx)


        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                f.close()
                ser.close()
                exit()
