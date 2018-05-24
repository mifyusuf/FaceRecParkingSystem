import os
import sys
import select
import glob
import cv2
import hardware
import config
import face
import UserData
import RPi.GPIO as GPIO

class CapturePose(object):
	def ReadCardID(self):
		global ID
		global camera
		global door
		global led
		User = UserData.UserData()
		ID = User.UserID()
		camera = config.get_camera()
		door =hardware.Door()
		led = hardware.Led()
	def cekDir(self):
		# Create the directory for positive training images if it doesn't exist.
		if not os.path.exists(config.TRAINING_DIR):
			os.makedirs(config.TRAINING_DIR)
		if not os.path.exists(config.POSITIVE_DIR):
			os.makedirs(config.POSITIVE_DIR)
		if not os.path.exists(config.POSITIVE_DIR + ID):
			os.makedirs(config.POSITIVE_DIR + ID)
		# Find the largest ID of existing positive images.
		# Start new images after this ID value.
	def CapturePic(self):
		files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR + ID, POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
		count = 0
		if len(files) > 0:
			# Grab the count from the last filename.
                        
			count = int(files[-1][-7:-4])+1
		print 'Capturing positive training images.'
		print 'Press button or type c (and press enter) to capture an image.'
		print 'Press Ctrl-C to quit.'
	
                while True:
                        if door.is_button_up() or is_letter_input('c'):
                                led.LedOn()
                                print 'Capturing image...'
                                image = camera.read()
                                # Convert image to grayscale.
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                                # Get coordinates of single face in captured image.
                                result = face.detect_single(image)
                                if result is None:
                                        print 'Could not detect single face!  Check the image in capture.pgm' \
                                                ' to see what was captured and try again with only one face visible.'
                                        continue
                                x, y, w, h = result
                                # Crop image as close as possible to desired face aspect ratio.
                                # Might be smaller if face is near edge of image.
                                crop = face.crop(image, x, y, w, h)
                                # Save image to file.
                                filename = os.path.join(config.POSITIVE_DIR + ID, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
                                cv2.imwrite(filename, crop)
                                print 'Found face and wrote training image', filename
                                led.LedOff()
                                count += 1
	def ListPose(self):
		pose_list = config.LIST_DIR + ID + '.pkl'
		folder_path = config.POSITIVE_DIR + ID
		List = UserData.UserData()
		List.WriteList(pose_list, folder_path)
# Prefix for positive training image filenames.

POSITIVE_FILE_PREFIX = 'positive_'

def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False


if __name__ == '__main__':
	try:
		CapturePose().ReadCardID()
		CapturePose().cekDir()
		CapturePose().CapturePic()
	except KeyboardInterrupt:
		GPIO.cleanup()
		execfile('admin.py')
		sys.exit()
