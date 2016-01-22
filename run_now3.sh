#!/bin/sh

#run interrupt
echo run G# print 'DHT.txt created'PIO interrupt
python3  /var/www/interrupt6.py  >/dev/null 2>&1&
echo  'DHT txt and csv created'
> DHT1.csv
> DHT1.txt
> DHT.txt
python   /home/pi/Adafruit_Python_DHT-master/examples/s3Upload2.py >/dev/null 2>&1&

echo run cloud_spreadsheet and iot mqtt publisher
python  /home/pi/Adafruit_Python_DHT-master/examples/cloud_spreadsheet_4_3.py


