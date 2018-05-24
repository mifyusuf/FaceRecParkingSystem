from time import sleep
import RPi.GPIO as GPIO

import cv2
import select
import sys
import config
import face
import hardware
import UserData
import os

# Initialize camer and box.
camera = config.get_camera()
door = hardware.Door()
led = hardware.Led()
	              
def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False
class Parking(object):
        def UserID(self):
                global ID
                User = UserData.UserData()
                ID = User.TrainData()       
                
        
        def IRstatus(self):
                sensorIR = config.INFRA_PIN
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(sensorIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                current = GPIO.input(sensorIR)
                previous = current
                while True:
                        current = GPIO.input(sensorIR)
                        if current != previous:
                                print current
                                door.lock()
                                return
        def LoadTrainData(self):
                # Load training data into model
                if not os.path.exists(config.TRAIN_DIR + ID):
                        print 'Kartu Tidak Terdaftar'
                        return Load()
                print 'Loading training data...'
                global model
                global trainfiles
                model = cv2.createEigenFaceRecognizer()
                trainfiles = os.path.join(config.TRAIN_DIR + ID, config.TRAINING_FILE)
                model.load(trainfiles)
                print 'Training data loaded!'

                
                # Move box to locked position.
                door.lock()
                print 'Running Lock...'
                print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
                print 'Press Ctrl-C to quit.'
        def FaceRec(self):
                while True:
                        
                                # Check if capture should be made.
                                # TODO: Check if button is pressed.
                                if door.is_button_up() or is_letter_input('l'):
                                        led.LedOn()
                                        if not door.is_locked:
                                                # Lock the door if it is unlocked
                                                door.lock()
                                                print 'Door is now locked.'
                                        else:
                                                print 'Button pressed, looking for face...'
                                                # Check for the positive face and unlock if found.
                                                image = camera.read()
                                                # Convert image to grayscale.
                                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                                                # Get coordinates of single face in captured image.
                                                result = face.detect_single(image)
                                                if result is None:
                                                        print 'Could not detect single face!  Check the image in capture.pgm' \
                                                                  ' to see what was captured and try again with only one face visible.'
                                                        sleep(.01)
                                                        continue
                                                x, y, w, h = result
                                                # Crop and resize image to face.
                                                crop = face.resize(face.crop(image, x, y, w, h))
                                                # Test face against model.
                                                label, confidence = model.predict(crop)
                                                print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
                                                        'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
                                                        confidence)
                                                if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
                                                        print 'Recognized face! Unlocking Door Now...'
                                                        door.unlock()
                                                        led.LedOff()
                                                        self.IRstatus()						
                                                        return self.main()							
                                                                                               
                                                else:
                                                        print 'Did not recognize face!'						
                                                        sleep(.01)
                                                        
        def main(self):
                self.UserID()
                self.LoadTrainData()
                self.FaceRec()


if __name__ == '__main__':
	try:
		Parking().main()
	except KeyboardInterrupt:
		door.clean()
		execfile('admin.py')
		sys.exit()
