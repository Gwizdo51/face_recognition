#from retinaface import RetinaFace
import cv2

def build_model():
    from retinaface import RetinaFace
    face_detector = RetinaFace.build_model()
    return face_detector

def detect_face(face_detector, img, align = True):
    
    from retinaface import RetinaFace
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #retinaface expects RGB but OpenCV read BGR
    
    face = None
    img_region = [0, 0, img.shape[0], img.shape[1]]

    faces = RetinaFace.extract_faces(img_rgb, model = face_detector, align = align)

    if len(faces) > 0:
        face = faces[0][:, :, ::-1]

    return face, img_region

def detect_faces(face_detector, img, align=True):

    img_regions_list = []
    
    from retinaface import RetinaFace

    # RetinaFace expects RGB but OpenCV read BGR
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # store the RGB images of the faces detected by RetinaFace in a list
    rgb_face_imgs = RetinaFace.extract_faces(img_rgb, model=face_detector, align=align)

    # convert the images back to BGR
    detected_faces_images = [cv2.cvtColor(rgb_face_img, cv2.COLOR_RGB2BGR) for rgb_face_img in rgb_face_imgs]

    # create the boxes and add them to img_regions_list
    if len(detected_faces_images) > 0:
        landmarks = RetinaFace.detect_faces(img_rgb, model=face_detector)
    
        for face_id in landmarks.keys():

            x1, y1, x2, y2 = landmarks[face_id]["facial_area"]
            x = x1
            y = y1
            w = x2 - x1
            h = y2 - y
            box = [x, y, w, h]

            img_regions_list.append(box)

    return detected_faces_images, img_regions_list