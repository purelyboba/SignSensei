from camera import VideoCamera
import cv2
from flask import Flask, render_template, Response

cam = VideoCamera()


if __name__ == '__main__':
#    while True:
#        image = cam.process_video()
#        cv2.imwrite('./public/bruh.jpg', image)
#        cv2.imshow("image", image)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
