# face_recognition

## TODO

- implement `DeepFaceWrapper` to handle the DeepFace module for Django. <ins>**DONE & TESTED**</ins>
- add a `last_analyzed_image` url, view and html <ins>**DONE & TESTED**</ins>
- add a HTML response for when the database is empty <ins>**DONE & TESTED**</ins>
- correct bug to `df_result` on Windows <ins>**DONE & TESTED**</ins>
- add `functions.resize_img_to_target_size` to resize a cv2 image to a target size
- modify `DeepFace.py` so that it analizes the image and draw the boxes separately
- post process `df_result` to compare it to a database of client, and draw green or red squares on the analyzed image based on whether they are allowed in or not
    - add a model `registered_clients`
    - fill the model with examples
    - for each row of `df_result`:
        - if the face is unknown, draw orange box
        - if the client is known and allowed in, draw green box
        - if the client is known and not allowed in, draw red box
- add a css page to group all common styles