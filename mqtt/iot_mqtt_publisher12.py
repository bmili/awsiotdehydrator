class iot_mqtt_publisher12:
        """A simple example class"""
        setPointTemp=43
        def __init__(self,thing,cert,tempin,tempout,curState,setPoint,humidity,weight, dtime):

		import ssl
		import paho.mqtt.client as mqtt
		import time
                import json
		self.tempout = tempout
		self.tempin = tempin
		#self.topic  = topic 
		self.humidity = humidity
		self.weight = weight
		self.curState    = curState
		self.cert    = cert
		self.thing    = thing
		self.dtime    = dtime
                self.message =""

	#called while client tries to establish connection with the server
		def on_connect(mqttc, obj, flags, rc):
		    if rc==0:
		        print ("Publisher Connection status code: "+str(rc)+" | Connection status: successful")
		    elif rc==1:
		        print ("Publisher Connection status code: "+str(rc)+" | Connection status: Connection refused")
                    mqttc.subscribe('$aws/things/FoodDehydratorTemperatureControl/shadow/update/accepted', qos=1)



		def on_publish(mqttc, userdata, mid):
		    print("mid: "+str(mid))

		def on_message(mosq, obj, msg):
		    global message
		    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
		    self.message = msg.payload
                    print(self.message)
                    j=json.loads(message)
                    #print json.dumps(j)
                    print( j["state"]["desired"]["setPoint"])
                    setPointTemp=j["state"]["desired"]["setPoint"]
                    if j["state"]["desired"]["setPoint"] !=44:
                       (rc, mid) = mqttc.publish('$aws/things/FoodDehydratorTemperatureControl/shadow/update' , "{ \"state\": {\"desired\": {\"setPoint\":44 } } }", qos=1)



		mqttc = mqtt.Client(client_id="FoodDehydrator-1")
		mqttc.on_publish = on_publish
		mqttc.on_connect = on_connect
		mqttc.on_message = on_message

		#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
		mqttc.tls_set("/home/pi/certificate/root-CA.crt",
	              certfile="/home/pi/certificate/"+cert+"certificate.pem",
        	      keyfile="/home/pi/certificate/"+cert+"private.pem",
	              tls_version=ssl.PROTOCOL_SSLv23,
        	      ciphers=None)


	#connecting to aws-account-specific-iot-endpoint
		mqttc.connect("A9HHD5G1IXZ9I.iot.eu-west-1.amazonaws.com", port=8883) #AWS IoT service hostname and portno
                if thing == 'FoodDehydratorTemperatureStatus':
 		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"intTemp\":"+str(tempin) +" }  } }", qos=1)
		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"extTemp\":"+str(tempout)+" }  } }", qos=1)
		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"curState\":"+curState   +" } } }", qos=1)
		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"weight\":"+str(weight)  +" } } }", qos=1)
		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"fromstart\":"+str(dtime)+" } } }", qos=1)
                else:
                 if setPoint !=None:
    		  (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"setPoint\":"+str(setPoint)+" } } }", qos=1)
    		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"enabled\":" +str(curState)+" } } }", qos=1)
		 (rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"desired\": {\"end\":"+str(dtime)+      " } } }", qos=1)    	

	#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"TEMPOUT\": "+str(tempout) +" } } }", qos=1)
    		#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"HUMIDITY\": "+str(humidity)+" } } }", qos=1)
    		#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"WEIGHT\": "+str(weight)+" } } }", qos=1)
    		#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"TEMPIN\": "+str(tempin)+" } } }", qos=1)
    		#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"TIME\": "+str(dtime )+" } } }", qos=1)
    		#(rc, mid) = mqttc.publish('$aws/things/'+thing+'/shadow/update' , "{ \"state\": {\"reported\": {\"FAN\": "\RUNNING\" } } }", qos=1)

import datetime
import time
TIME=datetime.datetime.now()
topic='$aws/things/BBQ/shadow/update'
tempin=33.6
tempout=22
humidity=27.55
weight=26.5
my_curState=["heating" ,"cooling","stopped"]
setPoint=43
cert='f03f954dd6-'
thing='FoodDehydratorTemperatureStatus'
thing='FoodDehydratorTemperatureControl'
my_array = ['FoodDehydratorTemperatureControl','FoodDehydratorTemperatureStatus']
for x in range(0, 13):
  if x==0:
   thing =my_array [0]
  else:
   thing =my_array [1]
  tempin=tempin+1
  tempout=tempout+1
  weight=weight-1
  humidity=humidity-1
  curState=my_curState[0]
  if thing == 'FoodDehydratorTemperatureStatus':
        time.sleep(10)
        dtime=datetime.datetime.now()-TIME
        #print(dtime.total_seconds() / 60.0)
        dtime=round((dtime.total_seconds() / 60.0),2)
  else:
        curState="true"#false" #true"
        dtime=800.0

  print thing 
  x= iot_mqtt_publisher12( thing,cert,tempin,tempout,curState,setPoint,humidity,weight,dtime)
  print ("curstate "+x.curState)
  print ("weight "+str(x.weight))
  print ("tempin "+str(x.tempin))
  print ("tempou "+str(x.tempout))
  print ("dtime "+str(x.dtime))
  print ("message "+x.message)
  if tempin > x.setPointTemp:
   curState=my_curState[2]
   x= iot_mqtt_publisher12( thing,cert,tempin,tempout,curState,setPoint,humidity,weight,dtime)
   print ("curState "+x.curState)
   print ("weight "+str(x.weight))
   print ("tempin  "+str(x.tempin))
   print ("tempou"+str(x.tempout))
   print ("dtime "+str(x.dtime))
   print ("setPointTem "+str(x.setPointTemp))

   curState="false" #true"
   thing =my_array [0]
   x= iot_mqtt_publisher12( thing,cert,tempin,tempout,curState,None,humidity,weight,dtime)
   print ("curState "+x.curState)
   print ("weight "+str(x.weight))
   print ("tempin "+str(x.tempin))
   print ("tempou "+str(x.tempout))
   print ("dtime "+str(x.dtime))
   print ("setPointTem "+str(x.setPointTemp))
   break

