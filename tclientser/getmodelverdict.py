import cv2
import mediapipe as mp
import numpy as np
import os
import csv
from keras.models import load_model

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

def modelpredict(coordinates):
    #coordinates to numpy
    narray = np.array([coordinates]).reshape(1, len(coordinates), -1)
    write_list_to_file("output.txt", coordinates)

    model = load_model('model.h5')

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    
    result = model.predict(narray)
    print(result, "MODEL RESULT")