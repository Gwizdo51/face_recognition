from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from numpy.random import randint, choice
# import time
from django.conf import settings
# from django.views import View
from pathlib import Path
import cv2
import os
import shutil
import pandas as pd
import numpy as np

print("loading DeepFace ...")
from deepface import DeepFace
from deepface.commons import functions
print("DeepFace is loaded")

from . import forms, models


def clear_cached_files(request):
    """
    This function clears the cached images and the model entries.
    """

    # delete media directory
    media_dir_path = settings.MEDIA_ROOT
    if media_dir_path.is_dir():
        shutil.rmtree(path=media_dir_path)

    # delete all entries in the model
    img_entries = models.UploadedImages.objects.all()
    print(f"deleting {len(img_entries)} entries")
    for img_entry in img_entries:
        img_entry.delete()

    return render(request, "home/cleared_cached_files.html")


class DeepFaceWrapper:
    """
    This wrapper handles the DeepFace module for django.
    """

    # choose another model or detector if you want to experiment:

    # 'VGG-Face', 'OpenFace', 'Facenet', 'Facenet512', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace'
    # ('Emotion', 'Age', 'Gender', 'Race') not implemented
    model_name = 'Facenet'
    recog_model = DeepFace.build_model(model_name)
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

        # get the path of the last analyzed image
        img_path = Path(image_db.uploaded_img.path)

        # put the name of the image in the model
        img_name = img_path.name
        image_db.img_name = img_name

        # analyze the image using the DeepFace module
        df_result = DeepFace.find_faces(
            img_path=img_path,
            db_path=settings.BASE_DIR / "database",
            model_name=cls.model_name,
            model=cls.recog_model,
            detector_backend=cls.detector,
            representations=cls.representations,
            verbose=True
        )

        # drop distance and best_match_path
        df_result = df_result.drop(columns=["distance", "best_match_path"])

        # add empty columns to match ClientDB
        df_result["date_of_birth"] = np.nan
        df_result["VIP"] = np.nan
        df_result["is_allowed_in"] = np.nan
        df_result["comments"] = np.nan
        df_result["total_entry_tickets_bought"] = np.nan
        df_result["creation_date"] = np.nan

        # complete df_result with data from ClientDB
        for client in models.ClientDB.objects.all():
            for index in df_result.index:
                if df_result.loc[index, "name"] == client.client_name:
                    df_result.loc[index, "date_of_birth"] = client.date_of_birth
                    df_result.loc[index, "VIP"] = client.VIP
                    df_result.loc[index, "is_allowed_in"] = client.is_allowed_in
                    df_result.loc[index, "comments"] = client.comments
                    df_result.loc[index, "total_entry_tickets_bought"] = client.total_entry_tickets_bought
                    df_result.loc[index, "creation_date"] = client.creation_date

        # load original image
        analyzed_img = cv2.imread(str(img_path))

        # resize it to standard size
        analyzed_img, ratio = functions.resize_img_to_target_size(analyzed_img)

        # draw boxes on the image
        for face_index in df_result.index:
            box = df_result.loc[face_index, "box"]
            name = df_result.loc[face_index, "name"]
            is_allowed_in = df_result.loc[face_index, "is_allowed_in"]
            if pd.isnull(name):
                # draw an orange box with the name "Unknown"
                analyzed_img = functions.draw_box(analyzed_img, box, ratio=ratio)
            else:
                if is_allowed_in:
                    # draw a green box
                    color = (0,255,0)
                else:
                    # draw a red box
                    color = (0,0,255)
                analyzed_img = functions.draw_box(analyzed_img, box, color=color, name=name.replace("_", " "), ratio=ratio)

        # save the analyzed image in MEDIA_ROOT/analyzed_images
        # (create the directory if it doesn't exist)
        analyzed_images_dir_path = Path(settings.MEDIA_ROOT / "analyzed_images")
        analyzed_img_path = analyzed_images_dir_path / img_name
        if not analyzed_images_dir_path.is_dir():
            print("no analyzed_images directory yet in media, creating")
            os.mkdir(path=analyzed_images_dir_path)
        cv2.imwrite(str(analyzed_img_path), analyzed_img)

        # drop "box" column and rows with null values
        df_result = df_result.drop(columns="box").dropna()

        # save df_result as a csv file in MEDIA_ROOT/analyzed_images
        csv_name = img_path.stem + ".csv"
        csv_path = analyzed_images_dir_path / csv_name
        df_result.to_csv(path_or_buf=str(csv_path), index=False)

        # save the model
        image_db.save()


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
            DeepFaceWrapper.analyze_uploaded_img()
            return redirect('/last_analyzed_image/')
        else:
            raise ValueError("form not valid ?")


def last_analyzed_image(request):
    """
    Shows the last analysed image.
    """

    try:
        # get the last entry in UploadedImages
        last_image_db = models.UploadedImages.objects.latest('id')

        # get the name of the last analyzed image and its corresponding csv
        img_name = last_image_db.img_name
        csv_name = Path(img_name).stem + ".csv"

        # load the csv with pandas
        csv_path = settings.MEDIA_ROOT / "analyzed_images" / csv_name
        df_result = pd.read_csv(filepath_or_buffer=str(csv_path))

        # format the DataFrame
        df_result["total_entry_tickets_bought"] = df_result["total_entry_tickets_bought"].astype('int32')
        df_result["date_of_birth"] = pd.to_datetime(df_result["date_of_birth"]).dt.strftime('%d %b %Y')
        df_result["creation_date"] = pd.to_datetime(df_result["creation_date"]).dt.strftime('%d %b %Y')

        last_analyzed_img_url = settings.MEDIA_URL + "analyzed_images/" + img_name
        context = {
            "db_is_empty": False,
            "analyzed_img_url": last_analyzed_img_url,
            "df_result": df_result.to_html(index=False).replace("_", " ")
        }

    except models.UploadedImages.DoesNotExist:
        context = {"db_is_empty": True}

    return render(request, "home/show_last_analyzed_image.html", context)
