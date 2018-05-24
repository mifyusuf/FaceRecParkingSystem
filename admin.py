import os
import sys
import time

try:
	user_input = raw_input("\n1. Capture Data \n2. Train Data \n3. Start ParkingSystem \nPilih Menu:")
	menu = user_input

	if menu == '1':
		execfile('CaptureFace.py')
	elif menu == '2':
		execfile('TrainData.py')
	elif menu == '3':
		execfile('parking.py')
    
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
   
