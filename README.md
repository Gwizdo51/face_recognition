# face_recognition

## TODO

- implement `DeepFaceWrapper` to handle the DeepFace module for Django. <ins>**DONE & TESTED**</ins>
- add a `last_analyzed_image` url, view and html <ins>**DONE & TESTED**</ins>
- add a HTML response for when the database is empty <ins>**DONE & TESTED**</ins>
- correct bug to `df_result` on Windows <ins>**DONE & TESTED**</ins>
- add `functions.resize_img_to_target_size` to resize a cv2 image to a target size <ins>**DONE & TESTED**</ins>
- make DeepFace store its weights in `deepface/model_weights/`
    - still to do: make face detectors store their weights there
- modify `DeepFace.py` so that it analizes the image and draw the boxes separately
- post process `df_result` to compare it to a database of client, and draw green or red squares on the analyzed image based on whether they are allowed in or not
    - add a model `registered_clients` <ins>**DONE & TESTED**</ins>
    - fill the model with examples <ins>**DONE & TESTED**</ins>
    - for each row of `df_result`:
        - if the face is unknown, draw orange box  <ins>**DONE & TESTED**</ins>
        - if the client is known and allowed in, draw green box  <ins>**DONE & TESTED**</ins>
        - if the client is known and not allowed in, draw red box  <ins>**DONE & TESTED**</ins>
- add post-process of `df_result` to display informations regarding the clients on `/last_analyzed_image/`  <ins>**DONE & TESTED**</ins>
- add a css page to group all common styles

## How to install with anaconda

(works on both Linux and Windows)

- clone the repository on your machine
- create a new virtual environment with **python 3.9**
- activate it
- `conda install -c conda-forge dlib`
- go the root of the repository
- `pip install -r requirements.txt`

## How to use

- go the root of the repository
- create the sqlite database file: `python manage.py migrate`<br>
this step might take a while as deepface will load and create representations for all the faces in the database directory.
- add fake informations about fake clients: `python create_client_db.py`
- run the django server: `python manage.py runserver`
- go to the url created by django and enjoy
