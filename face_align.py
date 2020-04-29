#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:54:35 2020

@author: alarazindancioglu
"""

from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
import os


'''
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
help="path to input image")
args = vars(ap.parse_args())




# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor and the face aligner
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
fa = FaceAligner(predictor, desiredFaceWidth=178, desiredFaceHeight=218, desiredLeftEye=(0.34,0.5))

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=800)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# show the original input image and detect faces in the grayscale
# image
cv2.imshow("Input", image)
rects = detector(gray, 2)

# loop over the face detections
for rect in rects:
	# extract the ROI of the *original* face, then align the face
	# using facial landmarks
	(x, y, w, h) = rect_to_bb(rect)
	faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
	faceAligned = fa.align(image, gray, rect)
    #cv2.imwrite("STGAN/STGAN/data/img_align_celeba/202600_align.jpg",faceAligned)
	# display the output images
    #cv2.imshow("Original", faceOrig)
	cv2.imwrite("STGAN/STGAN/data/img_align_celeba/202600_align.jpg", faceAligned)
	cv2.imshow("Aligned", faceAligned)
	cv2.waitKey(0)
    
'''

# =============================================================================
#BURASI FUNCTION OLARAK CAGIRMAK İÇİN  
# =============================================================================


def align_face(img_path):
    shape_pred='/Users/alarazindancioglu/Desktop/Comp537/shape_predictor_5_face_landmarks.dat'
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_pred)
    fa = FaceAligner(predictor, desiredFaceWidth=178, desiredFaceHeight=218, desiredLeftEye=(0.34,0.5))

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(img_path)
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # show the original input image and detect faces in the grayscale
    # image
    #cv2.imshow("Input", image)
    rects = detector(gray, 2)
    
    # loop over the face detections
    for rect in rects:
    	# extract the ROI of the *original* face, then align the face
    	# using facial landmarks
    	(x, y, w, h) = rect_to_bb(rect)
    	faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
    	faceAligned = fa.align(image, gray, rect)
        
        #cv2.imwrite("STGAN/STGAN/data/img_align_celeba/202600_align.jpg",faceAligned)
    	# display the output images
        #cv2.imshow("Original", faceOrig)
    	cv2.imwrite("STGAN/STGAN/data/img_align_celeba/202600.jpg", faceAligned)
    	pathAlign="STGAN/STGAN/data/img_align_celeba/202600.jpg"
        #cv2.imshow("Aligned", faceAligned)
    	cv2.waitKey(0)
        
    #return pathAlign


def divide_img(img_path, num_atts):
   #cwdir=os.getcwd()
   #os.chdir("/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/att_classification")
   #import imlib as im
   import numpy as np
   img_size=128
   img=cv2.imread(img_path)
   img = np.concatenate([img[:, :img_size, :], img[:, img_size+img_size//10:, :]], axis=1)
   img=np.expand_dims(img,axis=0)
   img=np.concatenate(np.split(img, 2, axis=2))
   
   path_orig="/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/output/128/sample_testing_divided/202600_orig.jpg"
   path_result="/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/output/128/sample_testing_divided/202600_result.jpg"
   
   #im.imwrite(img[0], path_orig)
   #im.imwrite(img[1], path_result)
   #os.chdir(cwdir)
   cv2.imwrite(path_orig, img[0])
   cv2.imwrite(path_result,img[1])
   
   return path_orig, path_result
   
    

