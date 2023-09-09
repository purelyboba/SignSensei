from flask import Flask, render_template, Response, jsonify
import camera
import cv2
import json

app = Flask(__name__)

videoStream = camera.VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = videoStream.process_video()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
     return Response(gen(videoStream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")

