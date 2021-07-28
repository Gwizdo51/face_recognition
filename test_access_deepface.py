import os
import sys
import pandas as pd
pd.set_option('display.max_colwidth', None)

from deepface import DeepFace


if __name__ == "__main__":
    df = DeepFace.find(img_path="../face_detection/test_images/test_chris.jpg", db_path="../face_detection/database")
    print(df.head())