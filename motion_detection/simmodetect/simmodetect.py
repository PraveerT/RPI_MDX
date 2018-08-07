#!/usr/bin/python

import picamera
import picamera.array
import time
import paho.mqtt.publish as publish
import datetime
threshold = 10    # How Much pixel changes
sensitivity = 100 # How many pixels change

def takeMotionImage(width, height):
    with picamera.PiCamera() as camera:
        time.sleep(1)
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

def scanMotion(width, height):
    motionFound = False
    data1 = takeMotionImage(width, height)
    while not motionFound:
        data2 = takeMotionImage(width, height)
        diffCount = 0;
        for w in range(0, width):
            for h in range(0, height):
                publish.single("iotdevice/connectionD", str(str(datetime.datetime.now())+" "+str(0)), hostname="iot.eclipse.org")
                # get the diff of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if  diff > threshold:
                    diffCount += 1
            if diffCount > sensitivity:
                break;
        if diffCount > sensitivity:
            motionFound = True
        else:
            data2 = data1
    return motionFound

def motionDetection():
    print ("Scanning for Motion threshold=%i sensitivity=%i..."  % (threshold, sensitivity))
    while True:
        if scanMotion(224, 160):
            publish.single("iotdevice/connectionD", str(str(datetime.datetime.now())+" "+str(1)), hostname="iot.eclipse.org")
            print ("Motion detected")

if __name__ == '__main__':
    try:
        motionDetection()
    finally:
        print ("Exiting Program")
