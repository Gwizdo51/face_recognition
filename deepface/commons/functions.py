import os
import numpy as np
import cv2
import base64
from pathlib import Path

# maybe not necessary
import sys
root_dir_path = str(Path(__file__).resolve().parent.parent.parent)
if root_dir_path not in sys.path:
    sys.path.insert(1, root_dir_path)

from deepface.detectors import FaceDetector

import tensorflow as tf
tf_version = int(tf.__version__.split(".")[0])

if tf_version == 1:
    from keras.preprocessing.image import load_img, save_img, img_to_array
    from keras.applications.imagenet_utils import preprocess_input
    from keras.preprocessing import image
elif tf_version == 2:
    from tensorflow.keras.preprocessing.image import load_img, save_img, img_to_array
    from tensorflow.keras.applications.imagenet_utils import preprocess_input
    from tensorflow.keras.preprocessing import image

#--------------------------------------------------

def initialize_input(img1_path, img2_path = None):

    if type(img1_path) == list:
        bulkProcess = True
        img_list = img1_path.copy()
    else:
        bulkProcess = False

        if (
            (type(img2_path) == str and img2_path != None) #exact image path, base64 image
            or (isinstance(img2_path, np.ndarray) and img2_path.any()) #numpy array
        ):
            img_list = [[img1_path, img2_path]]
        else: #analyze function passes just img1_path
            img_list = [img1_path]

    return img_list, bulkProcess

def initialize_weights_folder():

    # home = str(Path.home())

    # if not os.path.exists(home+"/.deepface"):
    #     os.mkdir(home+"/.deepface")
    #     print("Directory ",home,"/.deepface created")

    # if not os.path.exists(home+"/.deepface/weights"):
    #     os.mkdir(home+"/.deepface/weights")
    #     print("Directory ",home,"/.deepface/weights created")

    model_weights_dir_path = Path(__file__).resolve().parent.parent / "model_weights"
    # print(deepface_weights_path)

    if not model_weights_dir_path.is_dir() :
        os.mkdir(model_weights_dir_path)
        print("model weights directory created")

def loadBase64Img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def load_image(img):

    exact_image = False
    if type(img).__module__ == np.__name__:
        exact_image = True

    base64_img = False
    if len(img) > 11 and img[0:11] == "data:image/":
        base64_img = True

    #---------------------------

    if base64_img == True:
        img = loadBase64Img(img)

    elif exact_image != True: #image path passed as input
        if os.path.isfile(img) != True:
            raise ValueError("Confirm that ",img," exists")

        img = cv2.imread(img)

    return img

def detect_face(img, detector_backend = 'opencv', grayscale = False, enforce_detection = True, align = True):

    img_region = [0, 0, img.shape[0], img.shape[1]]

    #detector stored in a global variable in FaceDetector object.
    #this call should be completed very fast because it will return found in memory
    #it will not build face detector model in each call (consider for loops)
    face_detector = FaceDetector.build_model(detector_backend)

    detected_face, img_region = FaceDetector.detect_face(face_detector, detector_backend, img, align)

    if (isinstance(detected_face, np.ndarray)):
        return detected_face, img_region
    else:
        if detected_face == None:
            if enforce_detection != True:
                return img, img_region
            else:
                raise ValueError("Face could not be detected. Please confirm that the picture is a face photo or consider to set enforce_detection param to False.")

def preprocess_face(img, target_size=(224, 224), grayscale = False, enforce_detection = True, detector_backend = 'opencv', return_region = False, align = True):

    #img might be path, base64 or numpy array. Convert it to numpy whatever it is.
    img = load_image(img)
    base_img = img.copy()

    img, region = detect_face(img = img, detector_backend = detector_backend, grayscale = grayscale, enforce_detection = enforce_detection, align = align)

    #--------------------------

    if img.shape[0] == 0 or img.shape[1] == 0:
        if enforce_detection == True:
            raise ValueError("Detected face shape is ", img.shape,". Consider to set enforce_detection argument to False.")
        else: #restore base image
            img = base_img.copy()

    #--------------------------

    #post-processing
    if grayscale == True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #---------------------------------------------------
    #resize image to expected shape

    # img = cv2.resize(img, target_size) #resize causes transformation on base image, adding black pixels to resize will not deform the base image

    # First resize the longer side to the target size
    #factor = target_size[0] / max(img.shape)

    factor_0 = target_size[0] / img.shape[0]
    factor_1 = target_size[1] / img.shape[1]
    factor = min(factor_0, factor_1)

    dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
    img = cv2.resize(img, dsize)

    # Then pad the other side to the target size by adding black pixels
    diff_0 = target_size[0] - img.shape[0]
    diff_1 = target_size[1] - img.shape[1]
    if grayscale == False:
        # Put the base image in the middle of the padded image
        img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2), (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')
    else:
        img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2), (diff_1 // 2, diff_1 - diff_1 // 2)), 'constant')

    #double check: if target image is not still the same size with target.
    if img.shape[0:2] != target_size:
        img = cv2.resize(img, target_size)

    #---------------------------------------------------

    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255 #normalize input in [0, 1]

    if return_region == True:
        return img_pixels, region
    else:
        return img_pixels

def detect_faces(img, detector_backend='opencv', enforce_detection=False, align=True):

    # img_region = [0, 0, img.shape[0], img.shape[1]]

    # detector stored in a global variable in FaceDetector object.
    # this call should be completed very fast because it will return found in memory
    # it will not build face detector model in each call (consider for loops)

    face_detector = FaceDetector.build_model(detector_backend)

    detected_faces_images, img_regions_list = FaceDetector.detect_faces(face_detector, detector_backend, img, align)

    if len(detected_faces_images) >= 0:
        return detected_faces_images, img_regions_list
    else:
        if enforce_detection == False:
            return detected_faces_images, img_regions_list
        else:
            raise ValueError("Faces could not be detected. Please confirm that the picture contains facess or consider to set enforce_detection param to False.")

def preprocess_face_no_detection(img, target_size=(224, 224)):
    """
    input:
        img - cv2 processed numpy array representing the image
        taget_size - the input size of the model
    output:
        the input vector for the model
    """

    if img.shape[0] == 0 or img.shape[1] == 0:
        raise ValueError("Detected face image shape is ", img.shape,". Cannot preprocess.")

    #---------------------------------------------------
    #resize image to expected shape

    # img = cv2.resize(img, target_size) #resize causes transformation on base image, adding black pixels to resize will not deform the base image

    # First resize the longer side to the target size
    #factor = target_size[0] / max(img.shape)

    factor_0 = target_size[0] / img.shape[0]
    factor_1 = target_size[1] / img.shape[1]
    factor = min(factor_0, factor_1)

    dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
    img = cv2.resize(img, dsize)

    # Then pad the other side to the target size by adding black pixels
    diff_0 = target_size[0] - img.shape[0]
    diff_1 = target_size[1] - img.shape[1]
    img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2), (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')

    #double check: if target image is not still the same size with target.
    if img.shape[0:2] != target_size:
        img = cv2.resize(img, target_size)

    #---------------------------------------------------

    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255 #normalize input in [0, 1]

    return img_pixels

def find_input_shape(model):

    #face recognition models have different size of inputs
    #my environment returns (None, 224, 224, 3) but some people mentioned that they got [(None, 224, 224, 3)]. I think this is because of version issue.

    input_shape = model.layers[0].input_shape

    if type(input_shape) == list:
        input_shape = input_shape[0][1:3]
    else:
        input_shape = input_shape[1:3]

    if type(input_shape) == list: #issue 197: some people got array here instead of tuple
        input_shape = tuple(input_shape)

    return input_shape

def draw_box(img, box, color=(0,127,255), name="Unknown"):

    x, y, w, h = box
    x1 = x       # top left corner
    y1 = y
    x2 = x + w   # bottom right corner
    y2 = y + h

    img = cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=2)

    # bottom left corner of text string
    x3 = x
    y3 = y2 + 17
    org = (x3, y3)
    font = cv2.FONT_HERSHEY_DUPLEX
    img = cv2.putText(img, name, org, font, fontScale=.6, color=color, thickness=1, lineType=cv2.LINE_AA)

    # fonts: https://www.oreilly.com/library/view/mastering-opencv-4/9781789344912/16b55e96-1027-4765-85d8-ced8fa071473.xhtml
    # image for fonts: https://codeyarns.files.wordpress.com/2015/03/20150311_opencv_fonts.png
    # linetypes: https://www.oreilly.com/library/view/mastering-opencv-4/9781789344912/5c4150d2-b550-40be-8b18-f2e71e20d9be.xhtml

    return img

def draw_boxes(img, boxes, color=(0,127,255)):

    new_img = img.copy()

    for box in boxes:

        new_img = draw_box(new_img, box, color=color)

    return new_img

def resize_img_to_target_size(img_to_resize, target_width=1000, target_height=750):
    """
    This function either upscales or downscales the input image so that
    it meets the target size, while preserving its original aspect ratio.
    The resized image width and height will either be equal or smaller than
    the target width and height.
    """

    ratio_x = target_width / img_to_resize.shape[1]
    ratio_y = target_height / img_to_resize.shape[0]
    ratio = min(ratio_x, ratio_y)

    resized_img = cv2.resize(img_to_resize, (0,0), fx=ratio, fy=ratio)

    return resized_img


if __name__ == "__main__":
    pass
