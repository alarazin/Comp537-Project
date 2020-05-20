#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:18:04 2020

@author: alarazindancioglu
"""

from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2 
import os


def align_face(img_path, shape_pred, i): #stargan_dir eklenebilir
    detector=dlib.get_frontal_face_detector()
    predictor=dlib.shape_predictor(shape_pred)
    fa=FaceAligner(predictor, desiredFaceWidth=256, desiredFaceHeight=256, desiredLeftEye=(0.34, 0.5))
    image=cv2.imread(img_path)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects=detector(gray,2)
    
    for rect in rects:
        (x,y,w,h)=rect_to_bb(rect)
        faceOrig=imutils.resize(image[y:y+h, x:x+w], width=256)
        faceAligned=fa.align(image, gray, rect)
        
        cv2.imwrite("RaFD/test/neutral/img"+str(i)+".jpg", faceAligned)
        cv2.waitKey(0)
        

def divide_img(img_path, attr_num, base_dir=1, stargan_dir=1):
    import numpy as np 
    img_size=128
    img=cv2.imread(img_path)
    img_perf=img[128:256, :128, :]
    img=img[:128,:,:]
    img=np.expand_dims(img,axis=0)
    img=np.concatenate(np.split(img, 9, axis=2))
    
    #path_orig= os.path.join(base_dir, stargan_dir, "stargan_rafd/results_divided/img_orig.jpg")
    #path_result=os.path.join(base_dir, stargan_dir, "stargan_rafd/results_divided/img_target.jpg")
    path_orig= os.path.join("StarGAN/stargan_rafd/results_divided/img_orig.jpg")
    path_result=os.path.join("StarGAN/stargan_rafd/results_divided/img_target.jpg")
    
    
    cv2.imwrite(path_orig, img_perf)
    cv2.imwrite(path_result, img[attr_num])    
    return path_orig, path_result
