#rpi serial connections
#Python app to run a K-30 Sensor
import serial
import time
import serial
import time
import datetime
import json

import paho.mqtt.publish as publish
import time
import csv
ser = serial.Serial("/dev/serial0",baudrate =9600,timeout = .5)

ser.flushInput()
time.sleep(1)
while True:
    try:
    
        time.sleep(60)
        ser.flushInput()
        ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
        time.sleep(.5)
        resp = ser.read(7)
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high*256) + low
        print (co2)
        
        row=[str(datetime.datetime.now()),co2]
        dateraw=str(datetime.datetime.now())
        date=dateraw.split(' ')
        completemsg=date[0]+" "+date[1]+" "+str(co2)
        
        send_msg = {
                'co2': co2
        }
        with open('/home/pi/Desktop/sync/Conn+MQTT+PM2.5PM10/CO2.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow((row))

        csvFile.close()
            
        publish.single("iotdevice/connectionE", completemsg, hostname="iot.eclipse.org")
        publish.single("iotdevice/connectionEjson", payload=json.dumps(send_msg), hostname="iot.eclipse.org")
        print("Done")
    except:
        pass
        print ("error")
