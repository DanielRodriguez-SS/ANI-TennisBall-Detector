from PIL import Image
import cv2
import os
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
"""
https://safjan.com/convert-heic-and-heif-to-jpg-png-bmp-with-python/
"""
# Main

#print("Hola AI")

# By master god Daniel
#print('Python is cool')

def convert_heic_to_jpg(image_path:str):
    outfile_name = image_path.split('.')[-1]
    image = Image.open(image_path)
    image.convert('RGB').save(f'{outfile_name}.jpg')

if "__main__" == __name__:
    convert_heic_to_jpg('images/with_ball/IMG_6104.HEIC')