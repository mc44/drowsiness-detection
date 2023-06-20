import cv2
import mediapipe as mp
import numpy as np
import os
import csv
from keras.models import load_model
from notifypy import Notify
import time

HEADERSIZE = 10

def ExtractEyeAndMouthLandmarks(face_mesh, is3d):
        right_eye_landmarks = [33, 246, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
        left_eye_landmarks = [362, 382, 381, 380, 374, 373, 390, 249, 466, 388, 387, 386, 385, 384, 398]
        mouth_landmarks = [13, 14, 312, 317, 82, 87, 178, 402, 311, 81, 88, 95, 183, 42, 78, 318, 310, 324, 415, 308]
        lm_coord = [] 
        for facial_landmarks in face_mesh.multi_face_landmarks:
            landmarks = facial_landmarks.landmark
            for i, landmark in enumerate(landmarks):
                if i not in left_eye_landmarks and i not in right_eye_landmarks and i not in mouth_landmarks:
                    continue
                x = landmark.x
                y = landmark.y
                z = landmark.z
                if is3d:
                    lm_coord.append([x, y, z])
                else: 
                    lm_coord.append([x, y])

        return lm_coord

def write_list_to_file(file_name, data_list):
    with open(file_name, 'w') as file:
        for item in data_list:
            file.write(str(item) + '\n')

def pack(message):
    message = f'{len(message):<{HEADERSIZE}}' + message
    return message


#self.notification.message = f"No face detected for the last {frame_reset_threshold/30} seconds"
#self.notification.send()
def notify_client(verdict):
    status = ""
    notification = Notify()
    message_dict = {"Drowsy": "Are you alright? The model is detecting drowsiness", "No Face": "No face detected"}
    notification.title = "Status Detection"
    notification.message = message_dict[verdict]
    notification.send()

def modelpredict(coordinates, app, ip):
    #start_time = time.time()
    #coordinates to numpy
    narray = np.array([coordinates]).reshape(1, len(coordinates), -1)
    #write_list_to_file("output.txt", coordinates)

    model = load_model('gru_model.h5', compile=False)

    
    result = model.predict(narray)
    #end_time = time.time()
    #runtime = end_time - start_time
    #print(start_time, " ", end_time)
    #print(f"Runtime: {runtime} seconds")
    predicted_class = np.argmax(result)

    labels = ['Not Drowsy', 'Drowsy']
    verdict = labels[predicted_class]

    print(result, "MODEL RESULT")
    print(verdict, "MODEL RESULT")
    if verdict == "Drowsy":
        notify_client(verdict)
    app.connect_send("1",str(verdict))
    #app.server.send(bytes(pack("1"+f"{ip},"+str(verdict)), "utf-8"))