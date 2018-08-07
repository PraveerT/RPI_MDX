import serial
import time
import datetime
##ser = serial.Serial('/dev/ttyACM0',baudrate=115200)
##ser.flushInput()
import paho.mqtt.publish as publish
import time
import csv
a=[]
try:
    
    t = serial.Serial('/dev/ttyACM0',115200,
    timeout=59
                      )
except:
    t = serial.Serial('/dev/ttyACM1',115200,
    timeout=59)
while True:
    
    try:
   
        
        n=(t.read(100))
        rawdata=str(n.decode('utf-8'))[:-2]
        data=rawdata.split(',')
        if len(data)<3:
            
            ValueError("not the values we are looking for!") 
        print (rawdata)
        
        dateraw=str(datetime.datetime.now())
        date=dateraw.split(' ')
        completemsg=date[0]+" "+date[1]+" "+data[0]+","+data[1]+","+data[2]+","+data[3]+","+data[4]+","+data[5]+","+data[6]+","+data[7]+","+data[8]+","+data[9]+","+data[10]
        print (completemsg)
        
        row = [str(datetime.datetime.now()),data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]]
        print (row)
        with open('/home/pi/Desktop/sync/Conn+MQTT+PM2.5PM10/multichannel.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow((row))

        csvFile.close()
        
        publish.single("iotdevice/connectionC", completemsg, hostname="iot.eclipse.org")

        print("Done")
    except:
        pass
        print("error")

