#!/bin/sh

# print 'DHT.txt created'
#run interrupt
echo run GPIO interrupt
python  /var/www/interrupt6.py  >/dev/null 2>&1&

echo run cloud_spreadsheet , iotmqt publisher
python /home/pi/Adafruit_Python_DHT-master/examples/cloud_spreadsheet_4.py


