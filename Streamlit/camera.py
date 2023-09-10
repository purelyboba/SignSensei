import mediapipe as mp
import uuid
import numpy as np
import pandas as pd
import os
import random
import cv2
import tensorflow as tf
import time
import streamlit as st
import streamlit.components.v1 as components

cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
alphabets = list("ABCDEFGHIKLMNOPQRSTUVWXY")

model = tf.keras.models.load_model("newmodel.keras")
st.title("Lesson 1 - The Alphabet")
frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")


data = st.markdown('Loading...')
currentLetter = st.markdown('')
ct = st.markdown('')
tt = st.markdown('')

components.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    <script>
    </script>
    """,
)
# st.markdown('<span style="color:red">This text is red</span>', unsafe_allow_html=True)

st.session_state.correct_letter = None
correct_letter_start_time = None

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened() and not stop_button_pressed:
        if (st.session_state.correct_letter is None) or (st.session_state.correct_letter == "CORRECT"):
            # Generate a random letter if the correct letter has not been signed
            st.session_state.correct_letter = random.choice(alphabets)
            correct_letter_start_time = None  # Reset the start time for the next letter

            ct.text('')


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
            label_idx = np.argmax(model.predict(ll.reshape((1, -1))))
            label = alphabets[label_idx]
            print(label)
            frame_placeholder.image(image, channels="RGB")

            if label == st.session_state.correct_letter:
                if correct_letter_start_time is None:
                    correct_letter_start_time = time.time()

                tt.markdown(str(time.time() - correct_letter_start_time)[0:4])
                
                if time.time() - correct_letter_start_time >= 2.5:
                    st.session_state.correct_letter = "CORRECT"
                    ct.markdown('<span style="color:green;font-size:100px;">Correct! 😎</span>', unsafe_allow_html=True)
                    time.sleep(1)  # Add a small delay to display the "Correct!" message
                    st.session_state.correct_letter = None  # Reset the correct letter

            data.markdown("Current signed letter: " + label)

            if st.session_state.correct_letter is None:
                continue
            if label != st.session_state.correct_letter:
                currentLetter.markdown(f'<span style="color:orange;font-size:24px;">Your goal is to sign the letter: <span style="font-weight:900;">{st.session_state.correct_letter}</span>. <br />Once you sign the letter, hold your sign for 2.5 seconds to really start learning!</span>', unsafe_allow_html=True)
                correct_letter_start_time = None

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()