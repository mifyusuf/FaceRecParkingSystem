

import ParkingCard
import config
import os
import cPickle

class UserData(object):
	def UserID(self):
		kartu = ParkingCard.Card()
		UserID = kartu.Read()
		return UserID
	def TrainData(self):
		kartu = ParkingCard.Card()
		TrainDir = kartu.Read()
		return TrainDir

	def WriteList(self, pose_list, folder_path):
		if not os.path.exists(config.LIST_DIR):
			os.makedirs(config.LIST_DIR)
		with open(pose_list, "wb") as p:
			for path, subdirs, files in os.walk(folder_path):
				for filename in files:
					f = os.path.join(path, filename)
					cPickle.dump(str(f) + os.linesep, p)
                         
	def ReadList(self, pose_list, folder_path):
		with open(pose_list, "rb") as p:
			for path, subdirs, files in os.walk(folder_path):
				for filename in files:
					f = os.path.join(path, filename)
					print cPickle.load(p)
                         
