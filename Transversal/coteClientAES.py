# encoding: utf-8
import xxtea, requests, serial, time, sys
from influxdb import InfluxDBClient

'''
TODO: voir les tailles buffers dans le C, vérifier envoie/Récep
'''

#---------- VARS --------------
url = "https://emergencymanager.azurewebsites.net/fire/send"

SERIALPORT = "/dev/ttyUSB1"
BAUDRATE = 115200
ser = serial.Serial()

with open("keyFile.pem", "r") as fk:
    key = fk.readline()
    fk.close()

#---------- FUNCTIONS --------------
def initUART(state):
    if state == 'open':
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port = SERIALPORT
        ser.baudrate = BAUDRATE
        ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        ser.parity = serial.PARITY_NONE  # set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        ser.timeout = None  # block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False  # disable software flow control
        ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        # ser.writeTimeout = 0     #timeout for write
        print ("Starting Up Serial Monitor")
        try:
            ser.open()
        except serial.SerialException:
            print("Serial {} port not available".format(SERIALPORT))
            exit()
    elif state == 'close':
        ser.close()

def readUARTMessage():
    ret = ser.read(36) # lis X octets
    return ret    # on enleve le caractere de retour a la ligne pour decrypter 

def parseX(myStr):
    return myStr.replace("x", "")

def main():
    encryptedData = readUARTMessage()
    '''decrypted = xxtea.decrypt(encryptedData, key)
    for char in encryptedData:
        print char.encode('hex'),
    print('')'''
    print("encrypted " + encryptedData)
    #finalRet = parseX(str(decrypted))
    if(len(encryptedData) != 0):
        print("Feu déclenché: ")
        print(str(encryptedData))
        print(len(encryptedData))
        #myRequest = requests.post(url, data=finalRet)
        #print(myRequest.status_code)


#---------- WHILE TRUE --------------
initUART('open')
while(1):
    try:
        main()
    except KeyboardInterrupt:
        initUART('close')
        sys.exit()