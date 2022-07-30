#!/usr/bin/env python
from imutils.video import VideoStream
from flask import Flask, render_template, Response
import imutils
import time
import cv2
import json


app = Flask(__name__)
video_stream = VideoStream(src=0).start()
time.sleep(2.0)

point1 = []
point2 = []

        
@app.route('/')
def index():
    return render_template('test.html')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    def gen():
        while True:
            frame = video_stream.read()
            output_frame = imutils.resize(frame, width=400)
            output_frame = cv2.flip(output_frame, 1)
            # draw points if selected
            cv2.circle()
            output_frame = cv2.circle(output_frame, center_coordinates, radius, color, thickness)
            # encode the frame in JPEG format
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/click_data/<string:data>', methods=['POST'])
def ProcessClicData(data):
    coord = [ int(x) for x in data.split(',') ]
    if len(point1) == 2:
        point2 = coord
        
    else:
        point1 = coord   
         
    print(coord)
    return('/')



    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)