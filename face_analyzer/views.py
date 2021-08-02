from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from numpy.random import randint, choice
import time
from django.conf import settings
from django.views import View
from pathlib import Path

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

def test_show_lastest_uploaded_image(request):
    uploaded_img = models.UploadedImages.objects.latest('id')
    context = {"uploaded_image": uploaded_img}
    return render(request, "home/show_uploaded_image.html", context)

class Analyzer(View):

    print("class Analyzer is instanciated")

    from deepface import DeepFace
    model_name = 'Facenet'
    recog_model = DeepFace.build_model('Facenet')
    detector = 'mtcnn'
    representations = DeepFace.load_representations(
        db_path=settings.BASE_DIR / "database",
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

            img_to_analyze = models.UploadedImages.objects.latest('id')
            print(img_to_analyze.uploaded_img.path)
            name = img_to_analyze.uploaded_img.path.split("/")[-1]
            # print(name)
            # print(img_to_analyze.img_name)
            img_to_analyze.img_name = name
            img_to_analyze.save()



            # img_to_analyze.delete()
            
            context = {"uploaded_image": img_to_analyze.uploaded_img}
            return render(request, "home/show_uploaded_image.html", context)