# Raspberry Pi Temperature Controller

## Control a Air Heater Wirelessly over a Web or IOT Interface

This program will control an electric heating element in a dehydrator to set and regulate air temperature.  All status included temperature, humidity is logged localy to file  in CSV format to display on web  browser or android device wirelessly approx. every fwe seconds (sleep time).   The duty cycle and temperature is plotted in real time.  A Type C PID algorithm has been successfully implemented to automatically control the heating element when the desired temperature is set.  CSV  is transformed to  JSON file and both send to AWS S3 to display  temperature, humidity, weight diagram and spreadsheet for analytical purpose.  Status is also logged to AWS IOT to display on Android device and to control dehydrator by Android device. So there no need to run web server on Raspberry PI.

For bootstrap multi-heater and GPIO switch control version set template element to raspibrew_bootstrap.html in config.xml.  For original version set template to raspibrew.html.  The config.xml file explains how to setup for one, two or three heaters.  The number of heaters and GPIO switches can easily be expanded in the software.
The same raspidry.py code supports both versions.    

* Programmable [PID Controller]  for precise air heater temperature control
* Programmable  duty cycle time, and dry time
* Selectable options (Fruit, Fruit leather, Vegetables, Yoghurt making, Raising Bread
* Controllable from web browser, Android device (iPhone  coming soon) on Wifi network
* LCD readout for system status, toggle buttons for operation
* AWS S3 data archiving for analysing
* AWS IOT register a status of dehydrator and commands from Android device
* AWS Simple Notification Service (SNS) send an alarm, when temperature exceeded high level or process is interupted 
* Visualization Using Kibana


Hardware and Software Setup Information:  
[http://steve71.github.io/RasPiBrew/](http://steve71.github.io/RasPiBrew/)  

## Bootstrap Web Interface in Firefox Browser
<img src="https://github.com/steve71/RasPiBrew/raw/images/raspibrew_bootstrap.png" alt=""/>
## Original Web Interface in Firefox Browser
<img src="https://github.com/steve71/RasPiBrew/raw/images/PID_Tuning.png" alt="" width="954 height="476.5" /> 

----------

## Setting  

(https://github.com/steve71/RasPiBrew/raw/images/PID_Temp_Control.png)  
The temp plot shows temperature in degrees F over time in seconds.  
The heat plot shows duty cycle percentage over time in seconds.

## Hardware

A low cost credit card sized Raspberry Pi computer is an inexpensive and very expandable solution to controlling processes.  In our case heating process is controlled by measuring the   temperature, humidity and weight. Here we use it for temperature control of two heaters and two fans used in: dehydrator, dryer, <oghurt maker, bread rising heater.  Used in combination with a Smart    control relay ,   temperature sensors and a usb wifi dongle, a wirelessly controlled temperature controller can is developed.  The Raspberry Pi can run a web server to communicate the data to a browser or application on a computer or smartphone. In case of IOT, there is no need to run web server on RPI.  If you connect to  IOT , only Android device running android application you need.

Electronics used to test: Raspberry Pi, Raspberry Pi Plate kit from Adafruit, Smart  control relay  (4 chanell and GPIO starting vezje), a DS18B20 digital thermometer, 20x4 LCD and LCD117 kit (serial interface), 4.7k resistor, 1k resistor, 1N4001 diode, and 2N4401 transistor.  For wireless an Edimax EW-7811UN dongle is used.

Information on Raspberry Pi low-level peripherals:  
[http://elinux.org/RPi_Low-level_peripherals](http://elinux.org/RPi_Low-level_peripherals)


## Software

The language for the server side software is Python for rapid development.  The web server/framework is web.py.  Multiple processes connected with pipes to communicate between them are used.  For instance, one process can only get the temperature while another turns a heating element on and off.  A third parent temp control process can control the heating process with information from the temp process and relay the information back to the web server.

On the client side jQuery and various plugins can be used to display data such as line charts and gauges. Mouse overs on the temperature plot will show the time and temp for the individual points.  It is currently working in a Firefox and Chrome Browser.   

jQuery and two jQuery plugins (jsGauge and Flot) are used in the client:  
[http://jquery.com](http://jquery.com "jQuery")  
[http://code.google.com/p/jsgauge/](http://code.google.com/p/jsgauge/ "jsgauge")  
[http://code.google.com/p/flot/](http://code.google.com/p/flot/ "flot")  

The PID algorithm was translated from C code to Python.  The C code was from "PID Controller Calculus with full C source source code" by Emile van de Logt
An explanation on how to tune it is from the following web site:  
[http://www.vandelogt.nl/nl_regelen_pid.php](http://www.vandelogt.nl/nl_regelen_pid.php)  

The PID can be tuned very simply via the Ziegler-Nichols open loop method.  Just follow the directions in the controller interface screen, highlight the sloped line in the temperature plot and the parameters are automatically calculated.  After tuning with the Ziegler-Nichols method the parameters still needed adjustment because there was an overshoot of about 2 degrees in my system. I did not want the temperature to go past the setpoint since it takes a long time to come back down. Therefore, the parameters were adjusted to eliminate the overshoot.  For this particular system the Ti term was more than doubled and the Td parameter was set to about a quarter of the open loop calculated value.  Also a simple moving average was used on the temperature data that was fed to the PID controller to help improve performance.  Tuning the parameters via the Integral of Time weighted Absolute Error (ITAE-Load) would provide the best results as described on van de Logt's website above.

## Displaying 

