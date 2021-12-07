import serial
from datetime import datetime

def turnPumpOn(board:serial.Serial) -> None:
    """
    Writes to board to turn pump on
    
    :param board: The board from arduinoDriver
    """
    board.write(b'A')

def turnPumpOff(board:serial.Serial) -> None:
    """
    Writes to board to turn pump off
    
    :param board: The board from arduinoDriver
    """
    board.write(b'B')

def checkIfPumpNeeded(moisture: int, moistureLow: int, board: serial.Serial, floatFlag:bool, pumpStartTime:int, isPumpOn:bool) -> None:
    """
    Real simple function to check if the pump is needed or not, then turns it on or off accordingly

    :param moisture: The moisture level read from the sensor
    :param moistureLow: The lowest we allow the moisture to go
    :param board: The board from arduinoDriver
    """
    if floatFlag == 'HIGH':
        if isPumpOn:
            if moisture < moistureLow:
                turnPumpOn(board)
                return pumpStartTime, isPumpOn, False
            else:
                turnPumpOff(board)
                return pumpStartTime, False, True
        else:
            if moisture < moistureLow:
                turnPumpOn(board)
                return datetime.now(), True, False
            else:
                turnPumpOff(board)
                return pumpStartTime, isPumpOn, False
    else:
        turnPumpOff(board)
        if isPumpOn:
            return pumpStartTime, False, True
        return pumpStartTime, isPumpOn, False

