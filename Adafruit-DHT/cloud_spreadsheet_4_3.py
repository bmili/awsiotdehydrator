#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
#   sudo pip install gspread

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime

import Adafruit_DHT
import gspread

#from s3Upload1 import s3Upload1
from USBTempered import USBTempered

import RPi.GPIO as gpio  

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

#from oauth2client.client import GoogleCredentials


# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.AM2302

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN  = 4
# Example of sensor connected to Beaglebone Black pin P8_11
#DHT_PIN  = 'P8_11'

# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'boris@razmere.si'
GDOCS_PASSWORD         = 'nina1988'
GDOCS_SPREADSHEET_NAME = 'DHT Humidity Logi'
GDOCS_JSON             = '/home/pi/dht_master-57401b237121.json'
# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 10
COUNT                  = 30
#What draying is
SCALE=0.5
WEIGHT_TARA=1250*2
WEIGHT_TARA=3320
WEIGHT_TARA=1710
WEIGHT_TARA=2490
WEIGHT_TARA=490
TEMPHIGH = 42
TEMPLOW1  = 37
TEMPLOW  = 40
def login_open_sheet(json_file, spreadsheet1):
        #print ("spreadsheet: {}:".format(spreadsheet1)
        #try:
                #json_key = json.load(open(json))
        with open(json_file) as json_data:
                    json_key  = json.load(json_data)
            #print(json_key )

        #except:
                #print ('Unable to get json file '+ json+'.  Check json name.'
                #sys.exit(1)
        scope = ['https://spreadsheets.google.com/feeds']
        scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
#https://github.com/burnash/gspread/issues/224
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
#You'll need to add the email which was created with the JSON key to the spreadsheet you want to access. It will be something like 9876.....@developer.gserviceaccount.com. You'll find it as the "client email" in your JSON file and your credential page

         #credentials = SignedJwtAssertionCredentials(json_key['client_email'],  bytes(json_key['private_key'], 'utf-8'), scope=scope)
        gc = gspread.authorize(credentials)
        try:
        #worksheet = gc.open(spreadsheet).sheet1
         worksheet = gc.open(spreadsheet1).sheet1
        #worksheet = gc.open(spreadsheet).worksheet('sheet')
        #Date / TIme        Temperature %        Humidity %        Temperature out %        Weight (g)                                                                                                                                                                        
         return worksheet
        except:
                print ('Unable to get spreadsheet: {0}.  Check spreadsheet name.'.format(spreadsheet1).encode('utf-8'))
                #sys.exit(1)




print ('DHT1.txt created')
open('DHT1.txt', 'w').close()
                

#print ('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print ('Logging sensor measurements to {0} every {1} seconds.'.format("AWS S3 cloud", FREQUENCY_SECONDS+COUNT))
print ('Press Ctrl-C to quit.')
with open ('/var/www/cloud_spreadsheet_weight.txt', 'a') as f: f.write ('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)+"\n")
worksheet = None
PINZ = 21  # button 1 on webpage , rele 2
PINY = 22  # button 2 on webpage , rele 2
PINW = 23  # button 3 on webpage , rele 3, fan 220V
#PINR = 24  # button 4 on webpage , rele 4, fan 24V
PINX = 25  # button 5 on webpage , rele 6, fan 12V
gpio.setmode(gpio.BCM)  # broadcom mode  
gpio.setup(PINZ, gpio.OUT)
gpio.setup(PINY, gpio.OUT)
#gpio.setup(PINR, gpio.OUT)
gpio.setup(PINW, gpio.OUT)
gpio.setup(PINX, gpio.OUT)
#start fan 
print ('start fan & LOW temp ON')

with open ('/var/www/cloud_spreadsheet_weight.txt', 'a') as f: f.write ('Start fan\n')
# start fan 220 & 24V
gpio.output(PINW, gpio.HIGH)
#gpio.output(PINR, gpio.HIGH)
#start warmer with low temp
gpio.output(PINY, gpio.HIGH )


TIME                   = datetime.datetime.now()
counter=0
weight_1=0
try:
   while True:
        counter=counter+1

        #print ('Counter : '+str(counter)
        print ("Counter: {n}".format(n=str(counter)).encode('utf-8'))
        # Login if necessary.
        if worksheet is None:
                #worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)
                #worksheet = login_open_sheet_last(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)
                worksheet = login_open_sheet(GDOCS_JSON , GDOCS_SPREADSHEET_NAME)

        # Attempt to get sensor reading.
        humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)



        # Skip to the next reading if a valid measurement couldn't be taken.
        # This might happen if the CPU is under a lot of load and the sensor
        # can't be reliably read (timing is critical to read the sensor).
        #DHT senzor

        if humidity is None or temp is None:
                time.sleep(2)
                print ("humidity is null")
                #continue
                humidity=0.0
        else:
                print ('Humidity:    {0:0.1f} %'.format(humidity))
        if temp is None :
                time.sleep(2)
                print ("temp null")
                temp=0.0
                continue
        else:
                print ('Temperature: {0:0.1f} C'.format(temp))

        #humidity = 0.0
        #temp = 0.0
        tempcount = 0
        y= USBTempered()
        
        if y is None:
                print ("y is None")
                time.sleep(2)
                tempcount = tempcount +1
                #continue

        print ("Temperature in : {n} Temperature out : {m}".format(n=y.tempin, m=y.tempout).encode('utf-8'))
        if y.tempin is None:
                print ("y.tempin is None")
                time.sleep(2)
                tempcount = tempcount +1
                #continue
        if not (y.tempin):
                print ("no y.temp ")
                time.sleep(2)
                tempcount = tempcount +1
                #continue
        if (y.tempin).find('null') >0:
                print ("y.temp.find null ")
                time.sleep(2)
                tempcount = tempcount +1
                #continue
        if y.tempin==0.0:
                print( "y.tempin = "+y.tempin)
                time.sleep(2)
                tempcount = tempcount +1
                #continue
        tempout=float(y.tempout)
        tempin =float(y.tempin )
                
 
        # Append the data in the spreadsheet, including a timestamp
        print (' Append the data in the spreadsheet, including a timestamp')
        with open ('/var/www/cloud_spreadsheet.txt', 'a') as f: f.write ('Append the data in the spreadsheet, including a timestamp {k},{m},{n},{o}\r\n'.format(k=str(datetime.datetime.now()),m= str(temp),n=str(humidity),o= y.tempout))
        try:
                #worksheet.append_row((datetime.datetime.now(), temp, humidity,y.tempout,weight))
                worksheet.append_row((datetime.datetime.now(), temp, humidity,y.tempin ,'0'))
        except:
                # Error appending data, most likely because credentials are stale.
                # Null out the worksheet so a login is performed at the top of the loop.
                print ('Append error, logging in again')
                worksheet = None
                time.sleep(FREQUENCY_SECONDS)
                continue

        import sys
        sys.path.insert(0, '/home/pi/mqtt')
        from iot_mqtt_publisher1 import iot_mqtt_publisher1
        fan="heating"
        cert='f03f954dd6-'
        thing='FoodDehydratorTemperatureStatus'        
        weigth=0
        dtime=datetime.datetime.now()-TIME
        print("aws iot_mqtt_publisher")
        x= iot_mqtt_publisher1(thing, cert,temp,y.tempin ,humidity,weigth,fan,dtime)
        
        Bucketname = 'razmere.si'
        file='DHT'
        interval=3
        steps=60
        
        #x= s3Upload1(myfile,Bucketname,datetime.datetime.now(),temp,y.tempin,y.tempout,humidity,weight,interval,steps)
        #x= s3Upload1(myfile,Bucketname,datetime.datetime.now(),temp ,y.tempin,y.tempout,humidity,0,interval,steps)
        #line="\r\n"+str(datetime.datetime.now())+";"+str(round(temp,2))+";"+y.tempin+";"+y.tempout+";"+str(round(humidity,2))+";0"
        line="\r\n{k};{l};{m};{n};{o};{p}".format(k=str(datetime.datetime.now()),l=str(round(temp,2)),m=y.tempin,n=y.tempout,o=str(round(humidity,2)),p=0)
        #print("write to "+ file+"1.csv :" +line)
        print("write to {m} {n} to: ".format(m=line, n=file))
        with open( file+"1.csv", "a") as myfile:
                    myfile.write(line)
                    myfile.close()

        tab="        "
          #line=str(format(temp,'.2f'))+tab+y.tempin+tab+y.tempout+tab+str(round(humidity,2))+tab+str(round(weight,2))+"\r\n"
        line="{k}{t}{l}{t}{m}{t}{n}{t}{o}\r\n".format(k=str(format(temp,'.2f')),l=y.tempin,m=y.tempout,n=str(round(humidity,2)),o=0,t=tab)
        print("write {} to {}.txt".format(file, line))
        with open( file+".txt", "a") as myfile:
                    myfile.write(line)
                    myfile.close()

#        print datetime.datetime.now()
#        print ('Wrote a row {x.line} to {myfile}'
#        print ('Wrote a row  to {myfile}'
#        print ('Temperature: {0:0.1f} C'.format(temp)
#        print ('Humidity:    {0:0.1f} %'.format(humidity)
 

#check temp
        counter1=0;
        done=True
        while done:
                counter1=counter1+1
                print ('Count:{} count1: {} '.format(str(counter1),str(counter)))
                humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

                y= USBTempered()

                print ("tempin {}".format(y.tempin))
                if y is None:
                        time.sleep(2)
                        continue
                if (y.tempin).find('Could not open device') >0:
                        print('Could not open device')
                        time.sleep(2)
                        continue
                if y.tempin is None:
                        print ('y.tempin is None')
                        time.sleep(2)
                        continue
                if (y.tempin).find('null') >0:
                        print ('y.tempin ==null')
                        time.sleep(2)
                        continue
                if len(y.tempin)==0 :
                        print ('y.tempin ==0')
                        time.sleep(2)
                        continue
                if not (y.tempin):
                        print ("not y.temp ")
                        time.sleep(2)
                        continue
                if y.tempin < 0 :
                        print ('y.tempin < 0')
                        time.sleep(2)
                        continue
                tempout=float(y.tempout)
                tempin=float(y.tempin )

                if (temp > (1.1*TEMPHIGH)):
                #send alarm and exit
                        print (" exit: temp >{}".format(1.1*TEMPHIGH))
                        #print (" exit temp >"+str (1.1*TEMPHIGH)
                        with open ('/var/www/cloud_spreadsheet.txt', 'a') as f: f.write (' exit temp >'+str (1.1*TEMPHIGH))
                        sys.exit(1)
                if temp >= TEMPHIGH:
                          print ("1-First pin {} is low and second {} is low  when temp {} is more then {} ".format(PINY, PINZ, temp, TEMPHIGH+1))
                          gpio.output(PINY, gpio.LOW)
                          gpio.output(PINZ, gpio.LOW)
                elif temp < TEMPHIGH: # tempin >0: 
                        if  temp <  TEMPLOW1:
                                print ("2-First pin {} is high and second {} is high when temp {} is less then {} ".format(PINY, PINZ, temp, TEMPLOW1))
                                gpio.output(PINY, gpio.HIGH)
                                gpio.output(PINZ, gpio.HIGH)
                        elif temp > TEMPLOW1+3 and temp <  TEMPLOW:
                                print ("3-First pin {} is low and second {} is high when temp {} is less then {}".format(PINZ, PINY, temp, TEMPLOW ))
                                gpio.output(PINZ, gpio.LOW)
                                gpio.output(PINY, gpio.HIGH)

                        elif temp >= TEMPHIGH:
                                print ("4-First pin {} is low and second {} is high when temp {} is more then {}".format(PINZ, PINY, temp, TEMPHIGH))
                                gpio.output(PINZ, gpio.LOW)
                                gpio.output(PINY, gpio.HIGH)
                else:
                  print ("Exit if Temp    {} is less then  {} ".format(temp, 0))
                  sys.exit(1)


                print ('Temperature in :{}'.format(temp))
                #print ('Temperature check-in place '+str(temp) #y.tempin

                if counter1 == COUNT:
                  done=False
 
        if (temp > (1.1*TEMPHIGH)):
        #send alarm and exit
                print (" exit: tempin >{}".format(str (1.1*TEMPHIGH)))
                #print (" exit tempin >"+str (1.1*TEMPHIGH)
                with open ('/var/www/cloud_spreadsheet.txt', 'a') as f: f.write (' exit tempin >'+str (1.1*TEMPHIGH))
                sys.exit(1)
        # Wait 30 seconds before continuing
        time.sleep(FREQUENCY_SECONDS)

except KeyboardInterrupt:
     print ("\n", counter) # print value of counter  
finally:  
     gpio.cleanup() # this ensures a clean exit 
