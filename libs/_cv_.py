#!/usr/bin/python3
import cv2
import os
import numpy as np
from PIL import Image
from pickle import dump, load
from _sql_functions_ import sqlAppendActiveUser

#dirs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"user_images/")
cascade_dir = os.path.join(BASE_DIR,"cascades/")
if not os.path.exists(image_dir): os.makedirs(image_dir);
labels_path = os.path.join(image_dir, "labels.pcl")
model_path = os.path.join(image_dir, "model.yml")
#CV vars
users = []
labels = {}
font = cv2.FONT_HERSHEY_SIMPLEX;
color = (0, 255, 0);
stroke = 1;
cap = cv2.VideoCapture(0);
reco = cv2.face.createLBPHFaceRecognizer()
face_cascades = [\
    cv2.CascadeClassifier(cascade_dir+'frontal.xml'),\
    cv2.CascadeClassifier(cascade_dir+'frontal2.xml'),\
    cv2.CascadeClassifier(cascade_dir+'frontal3.xml'),\
    cv2.CascadeClassifier(cascade_dir+'frontal4.xml') ]

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
    for root, dirs, files in os.walk(image_dir):
        for f in files:
            if f.endswith('png') or f.endswith('jpg'):
                path = os.path.join(root,f)
                label = os.path.basename(root).replace(' ','_').lower()
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
    reco.train(x_train, np.array(y_labels))
    reco.save(model_path)

def addUserImage() -> None:
    name = input("enter the name of the user: ")
    user_dir = os.path.join(image_dir, "{}/".format(name))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    count = len(os.listdir(user_dir))+1
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, "press ENTER to save image\n press ESC to abort", (50, 50), font, stroke, color);
        cv2.imshow("frame", frame)
        faces = getFaces(gray);
        if len(faces) > 0:
            img = gray
            cv2.imshow("image", img)
        k = cv2.waitKey(1);
        if (k & 0xff in [ord('\r'), ord('\n')]):#enter
            cv2.imwrite("{}/{}.png".format(user_dir, count), img)
            count+=1;
            cv2.destroyWindow("image");
        elif (k &  0xff == 27 ):#escape
            break;
    trainModel();

def loadModel() -> None:
    global labels;
    reco.load(model_path);
    with open(labels_path, 'rb') as f:
        labels = {v:k for k, v in load(f).items()}

def closeCV() -> None:
    cap.release();
    cv2.destroyAllWindows();

def getUsersInFrame() -> [str]:
    global users;
    ret, frame = cap.read();
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    faces = getFaces(gray);
    for f in faces:
        for (x,y,w,h) in f:
            roi_g = gray[x:x+w, y:y+h]
            id_, conf = reco.predict(roi_g)
            if conf > 60 and labels[id_] not in users:
                sqlAppendActiveUser(labels[id_])

def getUsersInFrameAndShow() -> None:
    ret, frame = cap.read();
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    faces = getFaces(gray);
    for f in faces:
        for (x,y,w,h) in f:
            roi_g = gray[x:x+w, y:y+h]
            id_, conf = reco.predict(roi_g)
            if conf > 60:
                sqlAppendActiveUser(labels[id_])
                cv2.putText(frame, "{} {}".format(labels[id_],round(conf,3)), (x,y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2);
    cv2.imshow('frame', frame);
    if (cv2.waitKey(1) & 0xff == ord('q')):
        return -1
    return 1

def initCV() -> None:
    loadModel();
    
#if __name__ == "__main__":
    #while 1:
        #if getUsersInFrameAndShow() == -1: break;
     #   print(getUsersInFrame())
    #closeCV();
