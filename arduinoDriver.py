# Third Party
from datetime import datetime
import serial
import time

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.signalArduino import determineSignalToSend
from controllers.dataArray import DataArray
from controllers.database import Database

from classes import FloatSensor, Peripheral

board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
temp = 0
hum = 0
moisture = 0

thrashBool = True

lightArray = DataArray(101, 20)
moistureArray = DataArray(450, 5)

light_fixt = Peripheral(name="Light", critical_value=100)
pump = Peripheral(name="Pump", critical_value=450)


floatFlag = FloatSensor()
emailSent = False
emailTimestamp = 0

timeDataCollected = 0
lastMinuteSent = 1
envId = 1
signalSentBool = False

db = Database()

def checkIfEmailNeeded(floatFlag:FloatSensor, emailTimestamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - emailTimestamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if not floatFlag.flag and not emailSent:
        notifyLowWater(currentTime)
        emailSent = True
        emailTimestamp = time.time()
    if floatFlag.flag and emailSent:
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimestamp

while True:
    try:
        while(board.inWaiting() == 0):
            if temp != 0 and moisture != 0:
                # emailTimestamp = checkIfEmailNeeded(floatFlag, emailTimestamp)
                if temp != -999:
                    returned = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moistureArray.getAvg(),
                        light_fixt.calculate_time_on(), pump.calculate_time_on(), timeDataCollected, envId, db)
                    if returned != lastMinuteSent:
                        lastMinuteSent = returned
                        timeLightOn = 0
                        timePumpOn = 0
                if thrashBool:
                    light_fixt.evaluate_need(lightArray.getAvg())
                    pump.evaluate_need(moistureArray.getAvg())
                    thrashBool = False
                if not signalSentBool:
                    determineSignalToSend(pump.is_on, light_fixt.is_on, board)
                    signalSentBool = True
        timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        output = board.readline().decode('utf-8').strip().split(',')
        if len(output) == 6:
            temp = output[0]
            hum = output[1]
            moisture = int (output[2])
            moistureArray.add(moisture)
            lightArray.add(output[3])
            if 'LOW' in output[4]:
                floatFlag.set_low()
            else:
                floatFlag.set_high()
            thrashBool = True
            signalSentBool = False
            print(output)
        else:
            print("Incomplete board output: ", output)
            continue
    except Exception as error:
        print('**Error reading board: ', error)
