#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:32:02 2020

@author: alarazindancioglu
"""

import tensorflow as tf
from happybot import tf_helper
from happybot import facs_helper
from happybot import face_helper
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


'''
functiondan çıkardım
face_helper içinde shape_predictor path değiştirdim
file_low/file up 
'''




def extract_facs(img_path):
    dict_upper = ['AU1: Inner Brow Raiser','AU2: Outer Brow Raiser','AU4: Brow Lowerer','AU5: Upper Lid Raiser','AU6: Cheek Raiser','AU7: Lid Tightener']
    dict_lower = ['AU9: Nose Wrinkler', 'AU10: Upper Lip Raiser', 'AU12: Lip Corner Puller', 'AU15: Lip Corner Depressor',  'AU17: Chin Raiser',  'AU20: Lip Stretcher',  'AU23: Lip Tightener','AU24: Lip Pressor', 'AU25: Lips Part',  'AU26: Jaw Drop',  'AU27: Mouth Stretch']
    dict_emotion = ['Thinking...', 'Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']
    
    face_op = face_helper.faceUtil()
    vec = np.empty([68, 2], dtype = int)
    scaleFactor=0.4
    scaleUp=3/4
    width=256
    height=256
    centerFixed = np.array((int(width*scaleFactor / 2), int(height*scaleFactor /2) ))
    #centerFixed = np.array((int(width/2), int(height/2) ))
    #scale factor kaldırarak dene
    face_bool=False
    neutralBool=False
    
    tol=5
    
    
    file_low='happybot/nn/bottom/model-3000'
    file_up='happybot/nn/top/model-3000'
    
    #file_low='nn/bottom/model-3000'
    #file_up='nn/top/model-3000'
    
    modelLow=tf_helper.ImportGraph(file_low)
    modelUp=tf_helper.ImportGraph(file_up)
    
    #models are imported, how to run them?? 
    
    #im_list=['neutral.jpg','happy.jpg','angry.jpg', 'contemptuous.jpg','fearful.jpg','disgusted.jpg','surprised.jpg', 'sad.jpg']
    #im_list=['neutral.jpg', 'angry.jpg', 'contemptuous.jpg', 'disgusted.jpg', 'fearful.jpg', 'happy.jpg', 'sad.jpg', 'surprised.jpg']
    #im_list=['neutral.jpg','happy.jpg']
    im_list=['img0.jpg', 'img1.jpg']
    #subj='subjalara'
    #img_path='/Users/alarazindancioglu/Desktop/Comp537/RaFD/test/neutral'
    facsUp_save=[]
    facsLow_save=[]
    emo_save=[]
    
    for im in im_list:
        #image=cv2.imread(os.path.join(subj,im))
        image=cv2.imread(os.path.join(img_path, im))
        small_frame=cv2.resize(image,(0,0), fx=scaleFactor, fy=scaleFactor)
        #small_frame=cv2.resize(image,(0,0), fx=1, fy=1)
        face_bool=face_op.face_detect(small_frame,face_bool)
        
        if face_bool:
            vec, point, face_bool=face_op.get_vec(small_frame, centerFixed, face_bool)
            feat = facs_helper.facialActions(vec,small_frame)
            #plt.imshow(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))
            #plt.axis('off')
            #plt.figure()
            newFeaturesUpper = feat.detectFeatures()
            newFeaturesLower = feat.detectLowerFeatures()
            
            neutralBool, neutralFeaturesUpper, neutralFeaturesLower=face_op.set_neutral(feat, newFeaturesUpper, newFeaturesLower, neutralBool,tol)
        
        if neutralBool:
            facialMotionUp = np.reshape(feat.UpperFaceFeatures(neutralFeaturesUpper, newFeaturesUpper),(-1,19))
            facialMotionLow = np.reshape(feat.LowerFaceFeatures(neutralFeaturesLower, newFeaturesLower),(-1,6))
            
            facsLow = modelLow.run(facialMotionLow)
            facsUp = modelUp.run(facialMotionUp)
                        
            feel = tf_helper.facs2emotion(facsUp[0,:], facsLow[0,:])
            emotion = feel.declare()
            idxFacsLow = np.where(facsLow[0,:]==1)
            idxFacsUp = np.where(facsUp[0,:]==1)
            facsUp_save.append(idxFacsUp[0])
            facsLow_save.append(idxFacsLow[0])
            emos=[]
            for e in emotion:
                emos.append(dict_emotion[e])
                
            emo_save.append(emos)
        print('PIC DONE')
    return facsUp_save, facsLow_save, emo_save
    
    
    
