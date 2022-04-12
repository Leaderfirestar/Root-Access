# Third Party
from datetime import datetime
import logging

# Proprietary
from controllers.database import Database, SensorData, new_data_object
from controllers.powerConsumption import measurePowerConsumption
from controllers.waterConsumption import measureWaterConsumption

def checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, lightOnTimeSecs, pumpOnTimeSecs, timestamp, envId, db) -> datetime.minute:
    """If the time is right (every 15 minutes), calls send_data"""
    minutesToSendOn = [0, 15, 30, 45]
    now = datetime.now()
    minute = now.minute
    if minute in minutesToSendOn:
        if minute != lastMinuteSent:
            kwh = measurePowerConsumption(pumpOnTimeSecs, lightOnTimeSecs)
            ml = measureWaterConsumption(pumpOnTimeSecs)
            data = f'{envId},{timestamp},{lightOnTimeSecs},{ml},{kwh},{hum},{moisture},{temp}'
            logging.debug(" Sending data string: \n\t%s",
                data)
            send_data(data, db)
            lastMinuteSent = minute
    return lastMinuteSent

def send_data(data:str, db:Database) -> bool:
    """Sends data to database.
    Returns 1 if success, 0 otherwise."""
    data = new_data_object(data)
    try:
        db.Session.add(data)
        db.Session.commit()
        result = db.Session.query(SensorData).all()
        if result:
            logging.info(' Stored sensor data in database.')
        else:
            logging.error(' Failed to query database.')
    except Exception as error:
        logging.error(' Error adding to or querying database: %s',
            error)
        return 0
    return 1

if __name__ == '__main__':
    incoming = '0,2021-04-22 02:22:22,2,4,100,10,3'
    result = send_data(incoming, Database())
    assert result, "Failed to send data."
