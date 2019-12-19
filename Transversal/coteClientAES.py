# encoding: utf-8
import xxtea, requests, serial, time

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
    ret = ser.readline() # lis X octets
    return ret[:-1]      # on enleve le caractere de retour a la ligne pour decrypter 

def parseX(myStr):
    return myStr.replace("x", "")
#---------- WHILE TRUE --------------
while(1):
    initUART('open')
    encryptedData = readUARTMessage()
    decrypted = xxtea.decrypt(encryptedData, key)
    finalRet = parseX(decrypted)
    print("Feu déclenché: ")
    print(finalRet)
    myRequest = requests.post(url, data=finalRet)
    print(myRequest.status_code)
    initUART('close')