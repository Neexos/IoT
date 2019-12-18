# encoding: utf-8
from Crypto.PublicKey import RSA
import requests, serial


url = "https://cpefiresimulation.azurewebsites.net/send"
SERIALPORT = "/dev/ttyUSB1"
BAUDRATE = 115200
ser = serial.Serial()
'''
myRequest = requests.post(url, data="15,12,6;1,2,5")
print(myRequest.status_code)
print(myRequest.text)
'''

def initKeys():
    global pubKey
    global privateKey
    try:
        with open('publicSimu.pem', 'r') as fk:
            pub = fk.read()
            fk.close()
    except:
        print("erreur lors de la lecture du fichier 'publicSimu.pem'\n")
    try:
        with open('privateClient.pem', 'r') as fk:
            priv = fk.read()
            fk.close()
    except:
        print("erreur lors de la lecture du fichier 'privateClient.pem'\n")
    pubKey = RSA.importKey(pub)
    privateKey = RSA.importKey(priv)

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
    ret = ser.read(32) # lis 32 octets
    return str(ret)


initKeys()
while(1):
    initUART('open')
    encryptedData = readUARTMessage()
    decrypted = privateKey.decrypt(encryptedData)
    print(decrypted)
    initUART('close')

'''
conn = httplib.HTTPConnection(url, 80)
conn.request("POST", "45.2,55,8;")
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()
'''