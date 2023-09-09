import mediapipe as mp
import numpy as np
import cv2
import tensorflow as tf

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.alphabets = list("ABCDEFGHIKLMNOPQRSTUVWXY")

        self.model = tf.keras.models.load_model("newmodel.keras")

    def process_video(self):
        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
            while True:
                ret, frame = self.video.read()

                if not ret:
                    break

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
                # RGB 2 BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # Detections
                print(results)

                # Rendering results
                landmark_vertices_xyz = []
                temp_dataset = []
                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS,
                                                       self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2,
                                                                                  circle_radius=4),
                                                       self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                                  circle_radius=2),
                                                       )

                    for l in results.multi_hand_landmarks[0].landmark:
                        landmark_vertices_xyz.append(l.x)
                        landmark_vertices_xyz.append(l.y)
                        landmark_vertices_xyz.append(l.z)

                    temp_dataset.append(tuple(landmark_vertices_xyz))
                    ll = np.array(temp_dataset)
                    label_idx = np.argmax(self.model.predict(ll.reshape((1, -1))))
                    label = self.alphabets[label_idx]
                    print(label)


#                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    ret, jpeg = cv2.imencode('.jpg', image)
                    print(type(jpeg.tobytes()))
                    if jpeg.tobytes() is None:
                        continue
                    else:
                        return jpeg.tobytes()

#                return image


#                cv2.imshow('Hand Tracking', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        self.video.release()
        cv2.destroyAllWindows()

