import os
import zipfile
import bz2
import gdown
import numpy as np
from pathlib import Path

class DlibResNet:

	def __init__(self):

		#this is not a must dependency
		import dlib #19.20.0

		self.layers = [DlibMetaData()]

		#---------------------

		# home = str(Path.home())
		# weight_file = home+'/.deepface/weights/dlib_face_recognition_resnet_model_v1.dat'

		# #---------------------

		# #download pre-trained model if it does not exist
		# if os.path.isfile(weight_file) != True:
		# 	print("dlib_face_recognition_resnet_model_v1.dat is going to be downloaded")  

		# 	url = "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2"
		# 	output = home+'/.deepface/weights/'+url.split("/")[-1]
		# 	gdown.download(url, output, quiet=False)

		# 	zipfile = bz2.BZ2File(output)
		# 	data = zipfile.read()
		# 	newfilepath = output[:-4] #discard .bz2 extension
		# 	open(newfilepath, 'wb').write(data)

		# #---------------------

		# model = dlib.face_recognition_model_v1(weight_file)
		# self.__model = model

		model_weights_path = Path(__file__).resolve().parent.parent / "model_weights" / 'dlib_face_recognition_resnet_model_v1.dat'

		#download pre-trained model if it does not exist
		if not model_weights_path.is_file():
			print("downloading dlib_face_recognition_resnet_model_v1.dat...")  

			url = "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2"
			model_weights_zip_path = model_weights_path.parent / url.split("/")[-1]
			gdown.download(url, str(model_weights_zip_path), quiet=False)

			zip_file = bz2.BZ2File(str(model_weights_zip_path))
			data = zip_file.read()
			with open(model_weights_path, 'wb') as f:
				f.write(data)

		model = dlib.face_recognition_model_v1(str(model_weights_path))
		self.__model = model

		return None #classes must return None
	
	def predict(self, img_aligned):
		
		#functions.detectFace returns 4 dimensional images
		if len(img_aligned.shape) == 4:
			img_aligned = img_aligned[0]
		
		#functions.detectFace returns bgr images
		img_aligned = img_aligned[:,:,::-1] #bgr to rgb
		
		#deepface.detectFace returns an array in scale of [0, 1] but dlib expects in scale of [0, 255]
		if img_aligned.max() <= 1:
			img_aligned = img_aligned * 255
		
		img_aligned = img_aligned.astype(np.uint8)
		
		model = self.__model
		
		img_representation = model.compute_face_descriptor(img_aligned)
		
		img_representation = np.array(img_representation)
		img_representation = np.expand_dims(img_representation, axis = 0)
		
		return img_representation

class DlibMetaData:
	def __init__(self):
		self.input_shape = [[1, 150, 150, 3]]