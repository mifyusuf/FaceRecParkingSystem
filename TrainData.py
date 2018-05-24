import fnmatch
import os
import cv2
import numpy as np
import config
import face
import cPickle as pickle
import UserData

MEAN_FILE = 'mean.png'
POSITIVE_EIGENFACE_FILE = 'positive_eigenface.png'
NEGATIVE_EIGENFACE_FILE = 'negative_eigenface.png' 

if not os.path.exists(config.TRAIN_DIR):
	os.makedirs(config.TRAIN_DIR)
class TrainData(object):
        def walk_dir(self, path):        
                root, fold, files = os.walk(path).next()
                return fold
                                           
        def walk_files(self, directory, match='*'):
                """Generator function to iterate through all files in a directory recursively
                which match the given filename match parameter.
                """
                for root, dirs, files in os.walk(directory):
                        for filename in fnmatch.filter(files, match):
                                yield os.path.join(root, filename)

        def prepare_image(self, filename):
                """Read an image as grayscale and resize it to the appropriate size for
                training the face recognition model.
                """
                return face.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

        def normalize(self, X, low, high, dtype=None):
                #Normalizes a given array in X to a value between low and high.
                X = np.asarray(X)
                minX, maxX = np.min(X), np.max(X)
                # normalize to [0...1].
                X = X - float(minX)
                X = X / float((maxX - minX))
                # scale to [low...high].
                X = X * (high-low)
                X = X + low
                if dtype is None:
                        return np.asarray(X)
                return np.asarray(X, dtype=dtype)

              
                
        def main(self): 
                for fold in self.walk_dir(config.POSITIVE_DIR):                
                        if not os.path.exists(config.TRAIN_DIR + fold):
                                os.makedirs(config.TRAIN_DIR + fold)
                        print "Reading training images..."
                        faces = []
                        labels = []
                        pos_count = 0
                        neg_count = 0
                        count = 0
                        List = UserData.UserData()
                        pose_list = config.LIST_DIR + fold + '.pkl'
                        folder_path = config.POSITIVE_DIR
                        List.WriteList(pose_list, folder_path)
                        List.ReadList(pose_list, folder_path)
                        # Read all positive images
                        for filename in self.walk_files(config.POSITIVE_DIR + fold, '*.pgm'):
                                faces.append(self.prepare_image(filename))
                                labels.append(config.POSITIVE_LABEL)
                                pos_count += 1
                        # Read all negative images
                        for filename in self.walk_files(config.NEGATIVE_DIR, '*.pgm'):
                                faces.append(self.prepare_image(filename))
                                labels.append(config.NEGATIVE_LABEL)
                                neg_count += 1
                        print 'Read', pos_count, 'positive images and', neg_count, 'negative images.'

                        # Train model
                        print 'Training model...'
                        model = cv2.createEigenFaceRecognizer()
                        model.train(np.asarray(faces), np.asarray(labels))

                        # Save model results
                        trainfile = os.path.join(config.TRAIN_DIR + fold, config.TRAINING_FILE)
                        model.save(trainfile)
                        print 'Training data saved to', config.TRAIN_DIR + fold, config.TRAINING_FILE

                        # Save mean and eignface images which summarize the face recognition model.
                        meanfile = os.path.join(config.TRAIN_DIR + fold, MEAN_FILE)
                        positivefile = os.path.join(config.TRAIN_DIR + fold, POSITIVE_EIGENFACE_FILE)
                        negativefile = os.path.join(config.TRAIN_DIR + fold, NEGATIVE_EIGENFACE_FILE)
                        mean = model.getMat("mean").reshape(faces[0].shape)
                        cv2.imwrite(meanfile, self.normalize(mean, 0, 255, dtype=np.uint8))
                        eigenvectors = model.getMat("eigenvectors")
                        pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
                        cv2.imwrite(positivefile, self.normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
                        neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
                        cv2.imwrite(negativefile, self.normalize(neg_eigenvector, 0, 255, dtype=np.uint8))

                        count += 1
                else:
                        execfile('admin.py')

if __name__ == '__main__':
        TrainData().main()
        
