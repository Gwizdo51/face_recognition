import os
from pathlib import Path
import gdown
import zipfile

from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Convolution2D, LocallyConnected2D, MaxPooling2D, Flatten, Dense, Dropout

#-------------------------------------

def loadModel():
	base_model = Sequential()
	base_model.add(Convolution2D(32, (11, 11), activation='relu', name='C1', input_shape=(152, 152, 3)))
	base_model.add(MaxPooling2D(pool_size=3, strides=2, padding='same', name='M2'))
	base_model.add(Convolution2D(16, (9, 9), activation='relu', name='C3'))
	base_model.add(LocallyConnected2D(16, (9, 9), activation='relu', name='L4'))
	base_model.add(LocallyConnected2D(16, (7, 7), strides=2, activation='relu', name='L5') )
	base_model.add(LocallyConnected2D(16, (5, 5), activation='relu', name='L6'))
	base_model.add(Flatten(name='F0'))
	base_model.add(Dense(4096, activation='relu', name='F7'))
	base_model.add(Dropout(rate=0.5, name='D0'))
	base_model.add(Dense(8631, activation='softmax', name='F8'))

	#---------------------------------

	# home = str(Path.home())

	# if os.path.isfile(home+'/.deepface/weights/VGGFace2_DeepFace_weights_val-0.9034.h5') != True:
	# 	print("VGGFace2_DeepFace_weights_val-0.9034.h5 will be downloaded...")

	# 	output = home+'/.deepface/weights/VGGFace2_DeepFace_weights_val-0.9034.h5.zip'

	# 	gdown.download(url, output, quiet=False)

	# 	#unzip VGGFace2_DeepFace_weights_val-0.9034.h5.zip
	# 	with zipfile.ZipFile(output, 'r') as zip_ref:
	# 		zip_ref.extractall(home+'/.deepface/weights/')

	# base_model.load_weights(home+'/.deepface/weights/VGGFace2_DeepFace_weights_val-0.9034.h5')

	model_weights_path = Path(__file__).resolve().parent.parent / "model_weights" / 'VGGFace2_DeepFace_weights_val-0.9034.h5'

	if not model_weights_path.is_file():
		print("downloading VGGFace2_DeepFace_weights_val-0.9034.h5...")

		url = 'https://github.com/swghosh/DeepFace/releases/download/weights-vggface2-2d-aligned/VGGFace2_DeepFace_weights_val-0.9034.h5.zip'
		model_weights_zip_path = model_weights_path.parent / url.split("/")[-1]
		gdown.download(url, str(model_weights_zip_path), quiet=False)

		# unzip VGGFace2_DeepFace_weights_val-0.9034.h5.zip
		with zipfile.ZipFile(str(model_weights_zip_path), 'r') as zip_ref:
			zip_ref.extractall(str(model_weights_zip_path.parent))
	
	base_model.load_weights(str(model_weights_path))

	#drop F8 and D0. F7 is the representation layer.
	deepface_model = Model(inputs=base_model.layers[0].input, outputs=base_model.layers[-3].output)

	return deepface_model