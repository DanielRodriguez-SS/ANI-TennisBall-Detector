import cv2
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import pickle

DIR_PATH_WITH_BALL = 'images/with_ball/copies_jpg'
DIR_PATH_WITHOUT_BALL = 'images/without_ball/copies_jpg'
DIR_PATH_TO_MODEL = 'trained_model/model_01.pkl'

DIR_PATH_TO_IMAGE = 'images/with_ball/copies_jpg/IMG_6106.jpg'

def preprocess_image(image_path:str):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (244,244))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    #normalized_image = gray_image / 255.0
    normalized_image = gray_image
    return normalized_image

def extract_hog_features(image):
    hog = cv2.HOGDescriptor()
    hog_features = hog.compute(image)
    return hog_features.flatten()

def save_model(x_train, y_train):
    model = svm.SVC()
    model.fit(x_train, y_train)
    with open(DIR_PATH_TO_MODEL, 'wb') as file:
        pickle.dump(model, file)
    return model

def train_model():
    x = [] # Feature vectors
    y = [] # Labels

    with_ball_files = os.listdir(DIR_PATH_WITH_BALL)
    without_ball_files = os.listdir(DIR_PATH_WITHOUT_BALL)

    for file in with_ball_files:
        image = preprocess_image(f'{DIR_PATH_WITH_BALL}/{file}')
        hog_features = extract_hog_features(image)
        x.append(hog_features)
        y.append(1)

    for file in without_ball_files:
        image = preprocess_image(f'{DIR_PATH_WITHOUT_BALL}/{file}')
        hog_features = extract_hog_features(image)
        x.append(hog_features)
        y.append(0)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = save_model(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

def detect_object():
    with open(DIR_PATH_TO_MODEL, 'rb') as file:
        model = pickle.load(file)
    
    preprocessed_image = preprocess_image(DIR_PATH_TO_IMAGE)
    hog_features = extract_hog_features(preprocessed_image)

    label = model.predict([hog_features])[0]
    class_names = ['non tennis ball','tennis ball']
    predicted_class = class_names[label]
    print(f'Predicted Class: {predicted_class}')

    if predicted_class == 'tennis ball':
        #image = cv2.imread(DIR_PATH_TO_IMAGE)
        #cv2.imshow('Image detected',image)
        cv2.imshow('Image detected',preprocessed_image)
        cv2.waitKey(0)


def main():
    #train_model()
    detect_object()

if "__main__" == __name__:
    main()