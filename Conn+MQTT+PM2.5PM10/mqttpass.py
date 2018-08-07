# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
import time
import datetime
while True:
    try:
        time.sleep(20)
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
         
            # Subscribing in on_connect() - if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("iotdevice/connectionA")
            
         
        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            mydata=((msg.payload).decode('utf-8'))
            file = open("/usr/lib/python2.7/iotfiles/testfile.txt","a")
            file.write(str(datetime.datetime.now()))
            file.write(" ")
            file.write(mydata)
            
            print ("done")

        ##    if msg.payload == "Hello":
        ##        print("Received message #1, do something")
        ##        # Do something
        ##
        ##
        ##    if msg.payload == "World!":
        ##        print("Received message #2, do something else")
        ##        # Do something else
         
        # Create an MQTT client and attach our routines to it.
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
         
        client.connect("iot.eclipse.org", 1883, 60)
         
        # Process network traffic and dispatch callbacks. This will also handle
        # reconnecting. Check the documentation at
        # https://github.com/eclipse/paho.mqtt.python
        # for information on how to use other loop*() functions
        client.loop_forever()
    except:
        pass
