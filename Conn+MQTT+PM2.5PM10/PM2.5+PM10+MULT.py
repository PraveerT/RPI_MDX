import serial
import time
import datetime
##ser = serial.Serial('/dev/ttyACM0',baudrate=115200)
##ser.flushInput()
import paho.mqtt.publish as publish
import time
import csv



def hexShow(argv):  
    result = ''  
    hLen = len(argv)  
    for i in range(hLen):  
        hvol = argv[i]
        hhex = '%02x'%hvol  
        result += hhex+' '  
##    print ('hexShow:',result)
try:
    
    t = serial.Serial('/dev/ttyUSB0',9600)
except:
    t = serial.Serial('/dev/ttyUSB1',9600)

while True:
    try:
        time.sleep(60)
        t.flushInput()
        time.sleep(0.5)
        retstr = t.read(10)
        hexShow(retstr)
        if len(retstr)==10:
            if(retstr[0]==0xaa and retstr[1]==0xc0):
                checksum=0
                for i in range(6):
                    checksum=checksum+int(retstr[2+i])
                if checksum%256 == retstr[8]:
                    pm25=int(retstr[2])+int(retstr[3])*256
                    pm10=int(retstr[4])+int(retstr[5])*256
    ##                    print ("pm2.5:%.1f pm10 %.1f"%(pm25/10.0,pm10/10.0))

        #ser_bytes = ser.readline()
        #recoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        #msgtmqtt=(ser_bytes.decode('utf-8'))
        #print(msgtmqtt)
                    
        completemsg=str(datetime.datetime.now())+" "+str(pm25/10.0)+","+str(pm10/10.0)
        

        row = [str(datetime.datetime.now()), str(pm25/10.0), str(pm10/10.0)]

        with open('/home/pi/Desktop/sync/Conn+MQTT+PM2.5PM10/completedata.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()
        
       
        publish.single("iotdevice/connectionB", completemsg, hostname="iot.eclipse.org")

        print("Done")
    except:
        print ("error")
        pass
