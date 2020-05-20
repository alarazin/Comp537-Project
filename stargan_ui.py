#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:49:58 2020

@author: alarazindancioglu
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import os 
import argparse

from face_align_stargan import align_face, divide_img
sys.path.append('happybot')
from facs_trial import extract_facs

base_dir=os.getcwd()
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.setWindowTitle("Formative Feedback Generator")
        self.general_layout=QStackedLayout()
        #self.setFixedWidth(500)
        #self.setFixedHeight(500)
        
#PAGE 1 --INTRO
        page1=QVBoxLayout()
        self.description1= QLabel("Select the emotion you would like to express")
        page1.addWidget(self.description1)
        
        self.select_combo=QComboBox()
        self.combo_list=["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
        self.select_combo.addItems(self.combo_list)
        page1.addWidget(self.select_combo)
        #self.selected=self.select_combo.currentText()
        
        self.submit_btn=QPushButton("Submit")
        #self.btn1.clicked.connect(lambda n=1: general_layout.setCurrentIndex(n))
        self.submit_btn.clicked.connect(self.emotion_selection)
        self.submit_btn.clicked.connect(self.start_cam)
        
        page1.addWidget(self.submit_btn)
        
        widget1=QWidget()
        widget1.setLayout(page1)
        
#PAGE 2 --CAM
        self.cap=None
        self.page2=QVBoxLayout()
        #self.description2=QLabel(self.selected)
        #page2.addWidget(self.description2)
        
        self.cam_box=QLabel()
        self.page2.insertWidget(1, self.cam_box)
        
        self.capture_btn=QPushButton("Capture")
        self.capture_btn.clicked.connect(self.capture_img)
        #self.capture_btn.clicked.connect(self.results)
        self.page2.insertWidget(-2, self.capture_btn)
        
        self.return_btn=QPushButton("Return")
        self.return_btn.pressed.connect(self.return1)
        self.page2.insertWidget(-1,self.return_btn)
        
        self.img_count=0
        
        widget2=QWidget()
        widget2.setLayout(self.page2) 
              
#PAGE 3 --RESULTS
        self.page3_0=QHBoxLayout()
        self.page3_1=QVBoxLayout()
        self.page3_2=QVBoxLayout()
        self.page3_0.addLayout(self.page3_1)
        self.page3_0.addLayout(self.page3_2)
        
        widget3=QWidget()
        widget3.setLayout(self.page3_0)

#PAGE4 --CORRECT 
        self.page4=QVBoxLayout()
        #correct=QLabel('Your Performance is correct!')      
        self.page4.addWidget(QLabel('Your performance is correct!', alignment=Qt.AlignCenter))
        widget4=QWidget()
        widget4.setLayout(self.page4)
        
        
#Overall
        
        self.general_layout.addWidget(widget1)
        self.general_layout.addWidget(widget2)
        self.general_layout.addWidget(widget3)
        self.general_layout.addWidget(widget4)
        
        self.timer=QTimer(self,interval=5)
        self.timer.timeout.connect(self.update_frame)
        
        general_widget=QWidget()
        general_widget.setLayout(self.general_layout)
        self.setCentralWidget(general_widget)
        
    def emotion_selection(self):
        self.general_layout.setCurrentIndex(1)
        self.selected=self.select_combo.currentText()
        self.description2=QLabel("First capture Neutral then "+self.selected)
        self.page2.insertWidget(0,self.description2)
    
    def return1(self):
        self.general_layout.setCurrentIndex(0) 
        self.page2.removeWidget(self.description2)
        self.description2.hide()
        self.img_count=0
    
    def start_cam(self):
        if self.cap is None:
            self.cap=cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,200)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
        self.timer.start()
            
    def update_frame(self):
        ret,image=self.cap.read()
        img=cv2.flip(image,1)
        self.display_img(img,True)
    
    def display_img(self, img, window=True):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        outImg=QImage(img,img.shape[1], img.shape[0], img.strides[0], qformat)
        outImg=outImg.rgbSwapped()
        if window:
            self.cam_box.setPixmap(QPixmap.fromImage(outImg))
    
    def capture_img(self):
        flag, frame=self.cap.read()
        frame=cv2.flip(frame,1)
        path=os.path.join(base_dir,"test_imgs")
        if flag:
            QApplication.beep()
            name='img'+str(self.img_count)+'.jpg'
            cv2.imwrite(os.path.join(path,name), frame)
            self.img_count+=1
        selected=self.select_combo.currentText()
        print(selected)
        
        if self.img_count>1:
            for i in range(2):
                name_unaligned='img'+str(i)+'.jpg'
                align_face(os.path.join(path,name_unaligned), os.path.join(base_dir, "shape_predictor_5_face_landmarks.dat"),i)
        
            facsUp, facsLow, emo= extract_facs(os.path.join(base_dir, 'RaFD/test/neutral'))
            print(facsUp)
            print(facsLow)
            print(emo)
            #dict_upper = ['AU1: Inner Brow Raiser','AU2: Outer Brow Raiser','AU4: Brow Lowerer','AU5: Upper Lid Raiser','AU6: Cheek Raiser','AU7: Lid Tightener']
            #dict_lower = ['AU9: Nose Wrinkler', 'AU10: Upper Lip Raiser', 'AU12: Lip Corner Puller', 'AU15: Lip Corner Depressor',  'AU17: Chin Raiser',  'AU20: Lip Stretcher',  'AU23: Lip Tightener','AU24: Lip Pressor', 'AU25: Lips Part',  'AU26: Jaw Drop',  'AU27: Mouth Stretch']
            dict_upper = ['Raise inner brows','Raise outer brows','Lower Brows ','Raise Upper Lid','AU6: Cheek Raiser','AU7: Lid Tightener']
            dict_lower = ['Wrinkle nose', 'Raise upper lip', 'Pull lip corners up', 'Depress lip corners',  'Raise chin',  'Stretch lips',  'Tighten lips','Press lips', 'Part lips',  'Drop jaw',  'Stretch mouth']
            if selected in emo[1]:
                self.general_layout.setCurrentIndex(3)
                self.page4.insertWidget(-1, self.return_btn)
            else:
                self.general_layout.setCurrentIndex(2)
   
#BURAYI KALDIRABİLİRİZ 
                self.page3_1.addWidget(QLabel('You perform the following for '+selected.lower()+' :'))
                for up in facsUp[1]:
                    self.page3_1.addWidget(QLabel("  - " + dict_upper[up]))
                for low in facsLow[1]:
                    self.page3_1.addWidget(QLabel("  - " + dict_lower[low]))
 ###            

                emo_au={'Anger': [[2],[4, 6, 7]], 'Disgust': [[2],[0,3,4]], 'Fear': [[0,3],[5,8,9]], 'Happiness': [[],[2,8]], 'Sadness': [[0,2],[3,4]], 'Surprise': [[0,1,3],[8,9,10]]}
                self.page3_1.addWidget(QLabel('Try performing the following:'))
                for au_up in emo_au[selected][0]:
                    if au_up not in facsUp[1]:
                        self.page3_1.addWidget(QLabel("  - " + dict_upper[au_up]))
                for au_low in emo_au[selected][1]:
                    if au_low not in facsLow[1]:
                        self.page3_1.addWidget(QLabel("  - " + dict_lower[au_low]))
                
                self.page3_1.insertWidget(-1, self.return_btn)
                
                os.chdir('StarGAN')
                system_input="python main.py --mode test --dataset RaFD --image_size 128 --c_dim 8 --rafd_image_dir ../RaFD/test --sample_dir stargan_rafd/samples --log_dir stargan_rafd/logs --model_save_dir stargan_rafd/models --result_dir stargan_rafd/results"
                os.system(system_input)
                os.chdir(base_dir)
                
                emotion_list=["Input", "Anger", "Contempt", "Disgust", "Fear", "Happiness"," Thinking...","Sadness", "Surprise"]
                emo_idx=emotion_list.index(selected)
                path_orig, path_result= divide_img('StarGAN/stargan_rafd/results/1-images.jpg', emo_idx)
                
                
                self.user_perf=QLabel()
                self.user_perf.setPixmap(QPixmap(path_orig))
                self.user_perf.setAlignment(Qt.AlignCenter)
    
                self.corr_perf=QLabel()
                self.corr_perf.setPixmap(QPixmap(path_result))
                self.corr_perf.setAlignment(Qt.AlignCenter)
                
                self.page3_2.addWidget(QLabel("Your Performance", alignment=Qt.AlignCenter))
                self.page3_2.addWidget(self.user_perf)
                self.page3_2.addWidget(QLabel("Correct Performance", alignment=Qt.AlignCenter))
                self.page3_2.addWidget(self.corr_perf)
                
                
                
                
                
                
            
            
        
        
        
        
        
        
    # def results(self):
    #     if self.img_count>1:
    #         self.general_layout.setCurrentIndex(2)
    #         self.explanation=QLabel("Explanation")
    #         self.page3_1.addWidget(self.explanation)
    

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()

        