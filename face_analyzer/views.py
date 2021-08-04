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
print("loading deepface ...")
from deepface import DeepFace
print("deepface is loaded")

from . import forms, models

def index(request):
    context = {"firstname": "Arthur"}
    return render(request, 'home/index.html', context)

def random_int(request):
    context = {"number": randint(100)}
    return render(request, 'home/compute.html', context)

def api_test(request, username):
    return JsonResponse({"my d1ck": "my b@lls", "username": username})

def upload_img(request):
    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            img_to_analyze = models.UploadedImages.objects.latest('id')
            print(img_to_analyze.uploaded_img.path)
            context = {"uploaded_image": img_to_analyze.uploaded_img}
            return render(request, "home/show_uploaded_image.html", context)

    else:
        form = forms.ImageForm()
    return render(request, 'home/index.html', {'form': form})

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

class Analyzer(View):

    # 'VGG-Face', VGG-Face', 'OpenFace', 'Facenet', 'Facenet512', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace', 'Emotion', 'Age', 'Gender', 'Race'
    model_name = 'Facenet'
    recog_model = DeepFace.build_model('Facenet')
    # 'opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'
    detector = 'mtcnn'
    representations = DeepFace.load_representations(
        db_path=str(settings.BASE_DIR / "database"),
        model_name=model_name,
        model=recog_model,
        detector_backend=detector,
        verbose=True
    )

    # print((settings.BASE_DIR / "database").is_dir())
    # print(settings.BASE_DIR)
    # print(Path.cwd())
    
    def get(self, request):

        form = forms.ImageForm()
        return render(request, 'home/index.html', {'form': form})

    def post(self, request):

        form = forms.ImageForm(request.POST, request.FILES)
  
        if form.is_valid():
            
            form.save()

            image_db = models.UploadedImages.objects.latest('id')
            # print("#######################################")
            # print(repr(Path(image_db.uploaded_img.path).name))
            name = Path(image_db.uploaded_img.path).name
            image_db.img_name = name
            # image_db.save()
            # return HttpResponse('tests')

            # load the image with cv2
            # print(images.uploaded_img.url)
            # cv2_img = cv2.imread("./" + images.uploaded_img.url)
            
            # print(cv2_img.shape)
            # cv2.imshow('uploaded_img', cv2_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # analyze the image with find_faces
            df, analyzed_img = DeepFace.find_faces(
                img_path=str(Path(image_db.uploaded_img.path)),
                db_path=str(settings.BASE_DIR / "database"),
                model_name=self.model_name,
                model=self.recog_model,
                detector_backend=self.detector,
                representations=self.representations,
                verbose=True
            )
            print(df)

            # cv2.imshow('analyzed_img', analyzed_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # save the analyzed image to media/analyzed_images
            analysed_images_dir_path = Path(settings.MEDIA_ROOT / "analyzed_images")
            # print(str(analysed_images_dir_path))
            if not Path(settings.MEDIA_ROOT / "analyzed_images").is_dir():
                print("no analyzed_images directory yet in media, creating")
                os.mkdir(path=Path(settings.MEDIA_ROOT / "analyzed_images"))
            cv2.imwrite(str(analysed_images_dir_path / name), analyzed_img)

            image_db.save()
            # return HttpResponse('tests')

            # print(settings.MEDIA_URL + "analyzed_images/" + name)
            analyzed_img_url = settings.MEDIA_URL + "analyzed_images/" + name

            # analyzed_img_url = str(Path(images.uploaded_img.url).parent.parent / "analyzed_images" / images.img_name)
            context = {"analyzed_img_url": analyzed_img_url}
            return render(request, "home/show_analyzed_image.html", context)