#!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import paho.mqtt.client as mqtt
import json
message = 'ON'
def on_connect(mosq, obj, rc):
  #  mqttc.subscribe("f", 0)
    if rc==0:
		        print ("Publisher Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
		        print ("Publisher Connection status code: "+str(rc)+" | Connection status: Connection refused")

    print("rc: " + str(rc))
#    mqttc.subscribe("$aws/things/raspberrypi/shadow/update/#", qos=1)
    mqttc.subscribe('$aws/things/FoodDehydratorTemperatureControl/shadow/update/accepted', qos=1)


def on_message(mosq, obj, msg):
    global message
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    message = msg.payload
    print(    message)
    j=json.loads(message)
    #print json.dumps(j)
    print( j["state"]["desired"]["setPoint"])
    if j["state"]["desired"]["setPoint"] !=44:
      (rc, mid) = mqttc.publish('$aws/things/FoodDehydratorTemperatureControl/shadow/update' , "{ \"state\": {\"desired\": {\"setPoint\":44 } } }", qos=1)


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Connect
#mqttc.connect("localhost", 1883,60)


#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("/home/pi/certificate/root-CA.crt",
		certfile="/home/pi/certificate/bfe9fd14ce-certificate.pem",
		keyfile="/home/pi/certificate/bfe9fd14ce-private.pem",
                tls_version=ssl.PROTOCOL_SSLv23,
                ciphers=None)


#connecting to aws-account-specific-iot-endpoint
mqttc.connect("A9HHD5G1IXZ9I.iot.eu-west-1.amazonaws.com", port=8883) #AWS IoT service hostname and portno




# Continue the network loop
mqttc.loop_forever()