import mediapipe as mp
import uuid
import numpy as np
import pandas as pd
import os
import cv2
import tensorflow as tf
import time
from taipy import Gui

page = """
<|{image}|image|width=300px|height=300px|>
<|{prediction} prediction|>
"""

image = None
prediction = None

if __name__ == "__main__":
    Gui(page=page).run(dark_mode=True, port=8080)

cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
alphabets = list("ABCDEFGHIKLMNOPQRSTUVWXY")

model = tf.keras.models.load_model("newmodel.keras")

st.title("video hand capture")
frame_placeholder = st.empty()
txt = st.empty()
stop_button_pressed = st.button("Stop")


with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Flip on horizontal
        image = cv2.flip(image, 1)
        # Set flag
        image.flags.writeable = False
        # Detections
        results = hands.process(image)
        # Set flag to true
        image.flags.writeable = True
        # Detections
        print(results)
        
        if not ret:
            st.write("cap has ended")
            break


        # Rendering results
        landmark_vertices_xyz = []
        temp_dataset = []
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
#            print(results.multi_hand_landmarks)
            for l in results.multi_hand_landmarks[0].landmark:
                landmark_vertices_xyz.append(l.x)
                landmark_vertices_xyz.append(l.y)
                landmark_vertices_xyz.append(l.z)

            temp_dataset.append(tuple(landmark_vertices_xyz))
            ll = np.array(temp_dataset)
            label_idx = np.argmax(model.predict(ll.reshape((1,-1))))
            label = alphabets[label_idx]
            print(label)
            prediction = label
            frame_placeholder.image(image, channels="RGB")
            image = frame_placeholder

            page = """
            <|{image}image|width=300px|height=300px|>
            <|{prediction} prediction|>
            """

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()

