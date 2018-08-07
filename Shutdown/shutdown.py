
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time,os
import datetime
while True:
    try:
        
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            
         
            # Subscribing in on_connect() - if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("iotdevice/oscommand")
            
         
        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            mydata=((msg.payload).decode('utf-8'))
            p=os.popen(str(mydata))
            pp=[]
            pp.append(p.read())
            print (pp)
            publish.single("iotdevice/oscommandout", str(pp[0]), hostname="iot.eclipse.org")
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
         
        client.connect("iot.eclipse.org", 1883, 60)
        
        client.loop_forever()
    except:
        pass
