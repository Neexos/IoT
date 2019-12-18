# encoding: utf-8
from Crypto.PublicKey import RSA
import requests, time

#---------- VARS --------------
key = RSA.generate(1024)  # generation du couple de clefs
pubKey = key.publickey()  # clef publique
privateKey = key  # cle privee
url = "https://cpefiresimulation.azurewebsites.net/get"
myRequest = requests.get(url)
strt = time.time()
lystTest = '[["1","2","3"],["4","5","6"],["7","8","9"]]'
#--------- FUNCTIONS ----------
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
    elif state == close:
        ser.close()

def sendUARTMessage(msg):
    ser.write(msg.encode())

def encryptData(myString):
    encrypted = pubKey.encrypt(myString, 32)
    return encrypted

def getData(req):
    return req.text

def formatList(lst):
    lst = lst[1:-1]                             # On enlève les [] de debut/fin
    lst = lst.replace('[', '').replace(']', '') # on enlèce tous les autres []
    lst = lst.split('"')                        # on split selon les ""
    lst = list(filter(None, lst))               # supressions des valeurs null
    while (',' in lst):                         # suppressions des virgules
        lst.remove(",")
    return lst

def main(lst):
    formattedStr = ""
    # myList = formatList(lystTest)
    if myRequest.status_code == 200:
        data = getData(myRequest)
        data = formatList(data)
        count = 1
        for x in range(len(data)):
            if(count%3 != 0):
                formattedStr += data[x] + ','
            else:
                formattedStr += data[x] + ';\t'
            count += 1
        '''
        for x in range(len(myList)):
            if(count%3 != 0):
                formattedStr += myList[x] + ','
            else:
                formattedStr += myList[x] + ';\t'
            count += 1
        '''
        print(formattedStr)
        encryptedData = encryptData(formattedStr)
        decrypted = privateKey.decrypt(encryptedData)
        print(encryptedData)
        print(len(encryptedData[0]))
        print('\n')
        print(decrypted)
    else:
        print("Impossible de récupérer des données du serveur, code http: " + str(myRequest.status_code))
        time.sleep(2)

#-------- WHILE TRUE
while(1):
    main(lystTest)
    time.sleep(3)

'''
encryptedData = pubKey.encrypt(data, 32)

decrypted = privateKey.decrypt(encryptedData)
print(encryptedData)
print(len(encryptedData[0]))
print('\n')
print(decrypted)
end = time.time()
print("----- Execution time: " + str(end-strt) + " -----")
'''