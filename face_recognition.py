import cv2
import numpy as np
import os
import sqlite3
from PIL import Image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("recognizer/trainingData.yml")

#get profile by id from DB
def getProfile(id):
    conn = sqlite3.connect('data.db')
    query = "SELECT * FROM people WHERE ID="+ str(id)
    cusror = conn.execute(query)

    profile = None

    for row in cusror:
        profile = row

    conn.close()
    return profile

cap = cv2.VideoCapture(0)

fontface = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        roi_gray = gray[y: y+h, x: x+w]

        id, confidence = recognizer.predict(roi_gray)
        if confidence < 40:
            profile = getProfile(id)

            if (profile != None):
                cv2.putText(frame, ""+str(profile[1]), (x+10, y+h+30), fontface, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Unknown", (x+10, y+h+30), fontface, 1, (0,0,255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()