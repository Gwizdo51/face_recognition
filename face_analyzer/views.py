from functools import reduce
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from numpy.random import randint, choice
import time
from django.conf import settings
from django.views import View
from pathlib import Path
import cv2
import os
import shutil

import pandas as pd
print("loading DeepFace ...")
from deepface import DeepFace
print("DeepFace is loaded")

from . import forms, models


def clear_cached_files(request):

    # delete media directory
    media_folder_path = Path.cwd() / "media"
    print(str(media_folder_path))
    if media_folder_path.is_dir():
        shutil.rmtree(path=media_folder_path)

    # delete all entries in the model
    for img_entry in models.UploadedImages.objects.all():
        print(img_entry)
        img_entry.delete()

    return render(request, "home/cleared_cached_files.html")


class DeepFaceWrapper:
    """
    This wrapper handles the DeepFace module for django.
    """

    # 'VGG-Face', VGG-Face', 'OpenFace', 'Facenet', 'Facenet512', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace'
    # ('Emotion', 'Age', 'Gender', 'Race') not implemented
    model_name = 'Facenet'
    recog_model = DeepFace.build_model('Facenet')
    # 'opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'
    detector = 'mtcnn'
    representations = DeepFace.load_representations(
        db_path=settings.BASE_DIR / "database",
        model_name=model_name,
        model=recog_model,
        detector_backend=detector,
        verbose=True
    )

    @classmethod
    def analyze_uploaded_img(cls):
        """
        This method analyses the last uploaded image using DeepFace, and saves 
        the analyzed image in MEDIA_ROOT/analyzed_images
        """

        # get the last uploaded image from the model UploadedImages
        image_db = models.UploadedImages.objects.latest('id')

        # put the name of the image in the model
        name = Path(image_db.uploaded_img.path).name
        image_db.img_name = name
        
        # analyze the image using the DeepFace module
        df_result, analyzed_img = DeepFace.find_faces(
            img_path=Path(image_db.uploaded_img.path),
            db_path=str(settings.BASE_DIR / "database"),
            model_name=cls.model_name,
            model=cls.recog_model,
            detector_backend=cls.detector,
            representations=cls.representations,
            verbose=True
        )
        # print(df_result)

        # save the analyzed image in MEDIA_ROOT/analyzed_images
        # (create the directory if it doesn't exist)
        analyzed_images_dir_path = Path(settings.MEDIA_ROOT / "analyzed_images")
        if not Path(settings.MEDIA_ROOT / "analyzed_images").is_dir():
            print("no analyzed_images directory yet in media, creating")
            os.mkdir(path=Path(settings.MEDIA_ROOT / "analyzed_images"))
        cv2.imwrite(str(analyzed_images_dir_path / name), analyzed_img)

        # save the model
        image_db.save()

        # return df_result for post-processing
        return df_result


def index(request):
    """
    Home page. Allows the user to upload an image for analysis."
    """

    if request.method == 'GET':
        form = forms.ImageForm()
        return render(request, 'home/index.html', {'form': form})

    elif request.method == 'POST':

        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            df_result = DeepFaceWrapper.analyze_uploaded_img()
            return redirect('/last_analyzed_image/')
        else:
            raise ValueError("form not valid ?")


def last_analyzed_image(request):

    try:
        last_image_db = models.UploadedImages.objects.latest('id')

        name = last_image_db.img_name
        last_analyzed_img_url = settings.MEDIA_URL + "analyzed_images/" + name
        context = {"analyzed_img_url": last_analyzed_img_url, "db_is_empty": False}

    except models.UploadedImages.DoesNotExist:
        context = {"db_is_empty": True}

    return render(request, "home/show_last_analyzed_image.html", context)


# class Analyzer(View):

#     # 'VGG-Face', VGG-Face', 'OpenFace', 'Facenet', 'Facenet512', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace'
#     # ('Emotion', 'Age', 'Gender', 'Race') not implemented
#     model_name = 'Facenet'
#     recog_model = DeepFace.build_model('Facenet')
#     # 'opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'
#     detector = 'mtcnn'
#     representations = DeepFace.load_representations(
#         db_path=str(settings.BASE_DIR / "database"),
#         model_name=model_name,
#         model=recog_model,
#         detector_backend=detector,
#         verbose=True
#     )

#     # print((settings.BASE_DIR / "database").is_dir())
#     # print(settings.BASE_DIR)
#     # print(Path.cwd())
    

#     def get(self, request):

#         form = forms.ImageForm()
#         return render(request, 'home/index.html', {'form': form})


#     def post(self, request):

#         form = forms.ImageForm(request.POST, request.FILES)

#         if form.is_valid():
            
#             form.save()

#             image_db = models.UploadedImages.objects.latest('id')
#             # print("#######################################")
#             # print(repr(Path(image_db.uploaded_img.path).name))
#             name = Path(image_db.uploaded_img.path).name
#             image_db.img_name = name
#             # image_db.save()
#             # return HttpResponse('tests')

#             # load the image with cv2
#             # print(images.uploaded_img.url)
#             # cv2_img = cv2.imread("./" + images.uploaded_img.url)
            
#             # print(cv2_img.shape)
#             # cv2.imshow('uploaded_img', cv2_img)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()

#             # analyze the image with find_faces
#             df, analyzed_img = DeepFace.find_faces(
#                 img_path=str(Path(image_db.uploaded_img.path)),
#                 db_path=str(settings.BASE_DIR / "database"),
#                 model_name=self.model_name,
#                 model=self.recog_model,
#                 detector_backend=self.detector,
#                 representations=self.representations,
#                 verbose=True
#             )
#             print(df)

#             # cv2.imshow('analyzed_img', analyzed_img)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()

#             # save the analyzed image to media/analyzed_images
#             analysed_images_dir_path = Path(settings.MEDIA_ROOT / "analyzed_images")
#             # print(str(analysed_images_dir_path))
#             if not Path(settings.MEDIA_ROOT / "analyzed_images").is_dir():
#                 print("no analyzed_images directory yet in media, creating")
#                 os.mkdir(path=Path(settings.MEDIA_ROOT / "analyzed_images"))
#             cv2.imwrite(str(analysed_images_dir_path / name), analyzed_img)

#             image_db.save()
#             # return HttpResponse('tests')

#             # print(settings.MEDIA_URL + "analyzed_images/" + name)
#             analyzed_img_url = settings.MEDIA_URL + "analyzed_images/" + name

#             # analyzed_img_url = str(Path(images.uploaded_img.url).parent.parent / "analyzed_images" / images.img_name)
#             context = {"analyzed_img_url": analyzed_img_url}
#             return render(request, "home/show_analyzed_image.html", context)