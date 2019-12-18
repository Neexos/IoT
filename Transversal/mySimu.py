import serial

# send serial message 
# Don't forget to establish the right serial port ******** ATTENTION
SERIALPORT = "/dev/ttyUSB0" # port serie sur lequel on va ecrire
BAUDRATE = 115200
ser = serial.Serial()
urlSend = "https://emergencymanager.azurewebsites.net/fire/send" # envoyer au format X,Y,Z;A,B,C;
urlGet = "https://cpefiresimulation.azurewebsites.net/get"

def initUART():
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
    else:
        ser.close()


def sendUARTMessage(msg):
    ser.write(msg.encode())
    print("Message <" + msg + "> sent to micro-controller." )


def read_scales():
    # BOUCLE ENVOIS DES DONNEES
    for i in range(60):
        column = i - (i // 10) * 10
        row = i // 10
        if scales[i].get() > 0:
            print("Fire x=%d, y=%d has value %d" % (row, column, scales[i].get()))
        sendUARTMessage("%d%d%d\n\r" % (row, column, scales[i].get()))

def envois_de_test():
    sendUARTMessage("TLH")

initUART()