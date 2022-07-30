#!/usr/bin/env python
from imutils.video import VideoStream
from flask import Flask, render_template, Response
import imutils
import time
import cv2


app = Flask(__name__)
video_stream = VideoStream(src=0).start()
time.sleep(2.0)


        
@app.route('/')
def index():
    return render_template('test.html')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    def gen():
        while True:
            frame = video_stream.read()
            output_frame = imutils.resize(frame, width=400)
            # encode the frame in JPEG format
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)