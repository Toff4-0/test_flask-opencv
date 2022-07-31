#!/usr/bin/env python
from imutils.video import VideoStream
from flask import Flask, render_template, Response
import imutils
import time
import math
import cv2
import json

app = Flask(__name__)
video_stream = VideoStream(src=0).start()
time.sleep(2.0)



point1 = []
point2 = []
        
@app.route('/')
def index():
    return render_template('test.html', point1=point1,point2=point2)



@app.route('/video_feed', methods=['GET'])
def video_feed():
    def gen():
        while True:
            frame = video_stream.read()
            output_frame = imutils.resize(frame, width=400)
            output_frame = cv2.flip(output_frame, 1)
            # draw points if selected
            
            if len(point1) == 2:
                cv2.circle(output_frame, (point1[0],point1[1]), radius= (2), color=(0,0,255), thickness= 3)
                
            if len(point2) == 2:
                cv2.circle(output_frame, (point2[0],point2[1]), radius= (2), color=(0,0,255), thickness= 3)
            
            if (len(point1) == 2 & len(point2) == 2):
                cv2.line(output_frame, (point1[0],point1[1]), (point2[0],point2[1]), color=(0,0,255), thickness= 1)
                dist = math.sqrt((point2[0] - point1[0]) * (point2[0] - point1[0]) + (point2[1] - point1[1]) * (point2[1] - point1[1]))
                dist = round(dist,2)
                cv2.putText(output_frame, 'dist: '+ str(dist)+ ' px', (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0,0,255), thickness= 1)
            
            # encode the frame in JPEG format
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/click_data/<string:data>', methods=['POST'])
def ProcessClicData(data):
    global point1, point2
    if (len(point1) == 2 & len(point2) == 2):
        point1 = []
        point2 = []
        print("raz P1, P2")
        
    elif len(point1) == 2:
        point2 = [ int(x) for x in data.split(',') ]
        print("P2")
        print(point2)   
    
    else:
        point1 = [ int(x) for x in data.split(',') ]   
        point2 = [] 
        print("P1: ")
        print(point1)
        
    return render_template('test.html') 
   
@app.context_processor
def context_processor():
    global point1, point2
    return dict(point1=str(point1), point2=str(point2))


    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)