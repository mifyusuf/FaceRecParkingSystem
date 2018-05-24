#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

class Card(object):
    def Read(self):
        continue_reading = True
        MIFAREReader = MFRC522.MFRC522()
        # Welcome message
        print "Welcome to the MFRC522 data read example"
        print "Press Ctrl-C to stop."
     
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
	while continue_reading:
			
			# Scan for cards    
			(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

			# If a card is found
			if status == MIFAREReader.MI_OK:
				print "Card detected"
			
			# Get the UID of the card
			(status,uid) = MIFAREReader.MFRC522_Anticoll()

			# If we have the UID, continue
			if status == MIFAREReader.MI_OK:

				# Print UID
				
				CardID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
				print "Card read UID: ",CardID            
                                return CardID
				continue_reading = False
				

