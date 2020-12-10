# Person Pose Detector
#
# Detect human body, hand, facial and foot key points on an image. 
#
# @refer https://github.com/CMU-Perceptual-Computing-Lab/openpose
# @refer models: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/getModels.sh

import cv2
import numpy as np

protoFile = "pose/coco/pose_deploy_linevec.prototxt"
weightsFile = "pose/coco/pose_iter_440000.caffemodel"
nPoints = 18
POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

frame = cv2.imread('test.jpg')
frameWidth = frame.shape[1]
frameHeight = frame.shape[0]
threshold = 0.1

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368),
                          (0, 0, 0), swapRB=False, crop=False)

net.setInput(inpBlob)
output = net.forward()
points = []

for i in range(nPoints):
    minVal, prob, minLoc, point = cv2.minMaxLoc(output[0, i, :, :])
    if prob > threshold:
        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]
        cv2.circle(frame, (int(x), int(y)), 4, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
        points.append((int(x), int(y)))
    else :
        points.append(None)

for pair in POSE_PAIRS:
    partA = pair[0]
    partB = pair[1]
    if points[partA] and points[partB]:
        cv2.line(frame, points[partA], points[partB], (0, 255, 255), 1)

cv2.imshow('res', frame)
cv2.waitKey(0)