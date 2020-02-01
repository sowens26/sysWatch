#!/usr/bin/python3
from cv2 import destroyWindow, destroyAllWindows, VideoCapture, FONT_HERSHEY_SIMPLEX, COLOR_BGR2GRAY,\
        CascadeClassifier, waitKey, imshow, imwrite, rectangle, putText, cvtColor, LINE_AA
from cv2.face import LBPHFaceRecognizer_create
from os import path,makedirs,listdir, walk
from shutil import rmtree
import numpy as np
from PIL import Image
from pickle import dump, load
from _sql_functions_ import sqlAppendActiveUser, closeSqlConnection
from _globals_ import *

#dirs
BASE_DIR = path.dirname(path.abspath(__file__))
image_dir = path.join(BASE_DIR,"user_images/")
cascade_dir = path.join(BASE_DIR,"cascades/")
if not path.exists(image_dir): makedirs(image_dir);
labels_path = path.join(image_dir, "labels.pcl")
model_path = path.join(image_dir, "model.yml")
#CV vars
users = []
labels = {}
font = FONT_HERSHEY_SIMPLEX;
color = (0, 255, 0);
stroke = 1;
cap = VideoCapture(0);
reco = LBPHFaceRecognizer_create()
face_cascades = [\
    CascadeClassifier(cascade_dir+'frontal.xml'),\
    CascadeClassifier(cascade_dir+'frontal2.xml'),\
    CascadeClassifier(cascade_dir+'frontal3.xml'),\
    CascadeClassifier(cascade_dir+'frontal4.xml') ]

def getFaces(image_array) -> [tuple]:
    faces = [ face_cascades[0].detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5),\
        face_cascades[1].detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5),\
        face_cascades[2].detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5),\
        face_cascades[3].detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5) ]
    return faces 

def trainModel() -> None:
    id_c = 0 # counter
    label_ids = {}
    x_train, y_labels = [],[]
    for root, dirs, files in walk(image_dir):
        for f in files:
            if f.endswith('png') or f.endswith('jpg'):
                path = path.join(root,f)
                label = path.basename(root).replace(' ','_').lower()
                if label not in label_ids:
                    label_ids[label] = id_c
                    id_c += 1
                _id = label_ids[label]
                img = Image.open(path).convert('L')
                image_array = np.array(img, 'uint8')
                faces = getFaces(image_array);
                for f in faces:
                    for (x,y,w,h) in f:
                        roi = image_array[y:y+h, x:x+h]
                        x_train.append(roi)
                        y_labels.append(_id)   
    with open(labels_path, 'wb') as f:
        dump(label_ids, f)
    try:
        reco.train(x_train, np.array(y_labels))
    except:
        helpMessage();
        print("no user images found");
        addUserImage();
    reco.save(model_path)
    print("recognition model trained");

def addUserImage() -> None:
    name = input("enter the name of the user: ")
    print("press ENTER to save an image, press ESC when you're finished")
    user_dir = path.join(image_dir, "{}/".format(name))
    if not path.exists(user_dir):
            makedirs(user_dir)
    count = len(listdir(user_dir))+1
    while True:
        ret, frame = cap.read()
        gray = cvtColor(frame, COLOR_BGR2GRAY)
        putText(frame, "press ENTER to save image\n press ESC to abort", (50, 50), font, stroke, color);
        faces = getFaces(gray);
        if len(faces) > 0:
            img = gray
            imshow("image", img)
        k = waitKey(1);
        if (k & 0xff in [ord('\r'), ord('\n')]):#enter
            imwrite("{}/{}.png".format(user_dir, count), img)
            print("images saved to {}/{}.png".format(user_dir, count))
            count+=1;
            destroyWindow("image");
        elif (k &  0xff == 27 ):#escape
            if count == 0:
                rmtree(image_dir)
                print("no user added");
                exit();
            else:
                break;
    destroyWindow("image")
    trainModel();
    exit();
    
def loadModel() -> None:
    global labels;
    try:
        reco.read(model_path);
    except:
        trainModel()
        reco.read(model_path)
    with open(labels_path, 'rb') as f:
        labels = {v:k for k, v in load(f).items()}
    print("recognition model loaded");

def getUsersInFrame() -> [str]:
    global users;
    ret, frame = cap.read();
    gray = cvtColor(frame, COLOR_BGR2GRAY);
    faces = getFaces(gray);
    for f in faces:
        for (x,y,w,h) in f:
            roi_g = gray[x:x+w, y:y+h]
            id_, conf = reco.predict(roi_g)
            if conf > 60 and labels[id_] not in users:
                sqlAppendActiveUser(labels[id_])

def getUsersInFrameAndShow() -> None:
    ret, frame = cap.read();
    gray = cvtColor(frame, COLOR_BGR2GRAY);
    faces = getFaces(gray);
    for f in faces:
        for (x,y,w,h) in f:
            roi_g = gray[x:x+w, y:y+h]
            id_, conf = reco.predict(roi_g)
            if conf > 60 and labels[id_] not in users:
                sqlAppendActiveUser(labels[id_])
                putText(frame, "{} {}".format(labels[id_],round(conf,3)), (x,y), font, 1, color, stroke, LINE_AA)
                rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2);
    imshow('frame', frame);
    if (waitKey(1) & 0xff == 27):
        closeSqlConnection();
        closeCV();
        exit();

def initCV() -> None:
    loadModel();

def closeCV() -> None:
    cap.release();
    destroyAllWindows();

