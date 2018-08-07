import serial
ser = serial.Serial('/dev/ttyACM1',baudrate=115200)
ser.flushInput()
import paho.mqtt.publish as publish
import time

time.sleep(10)

while True:
    try:

        ser_bytes = ser.readline()
        #recoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        msgtmqtt=(ser_bytes.decode('utf-8'))
        print(msgtmqtt)
        
        publish.single("iotdevice/connectionA", msgtmqtt, hostname="iot.eclipse.org")

        print("Done")
    except:
        pass
