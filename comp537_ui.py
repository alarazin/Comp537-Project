#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:54:21 2020

@author: alarazindancioglu
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import os 

from face_align import align_face, divide_img



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.setWindowTitle("Cam Trial")
        general_layout=QStackedLayout()
        page1_layout= QHBoxLayout() 
        page1_1_layout=QVBoxLayout()
        page1_2_layout=QVBoxLayout()
        
        page2=QLabel("Hello")
        
        self.select_combo=QComboBox()
        self.combo_list=["Select","Bald", "Bangs", "Black_Hair", "Blond_Hair", "Brown_Hair", "Bushy_Eyebrows", "Eyeglasses", "Male", "Mouth_Slightly_Open", "Mustache", "No_Beard", "Pale_Skin", "Young"]
        self.select_combo.addItems(self.combo_list)

        self.select_combo.currentIndexChanged.connect(self.start_cam)
        
    
        self.cap=None
        
        page1_2_layout.addWidget(self.select_combo)


        self.cam_box=QLabel()
        page1_1_layout.addWidget(self.cam_box)
        
        capture_button=QPushButton("Capture")
        capture_button.clicked.connect(self.capture_img)
        capture_button.clicked.connect(self.window_change)
        page1_1_layout.addWidget(capture_button)
        
        
        page1_layout.addLayout(page1_2_layout)
        page1_layout.addLayout(page1_1_layout)
        

        
        self.timer=QTimer(self,interval=5)
        self.timer.timeout.connect(self.update_frame)
        
        widget=QWidget()
        widget.setLayout(page1_layout)
        self.setCentralWidget(widget)
        self.img_count=0
    
        
        
    def start_cam(self,i):
        if i!=0 :
            if self.cap is None:
                self.cap=cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,200)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,200)
            self.timer.start()
                            
                
    def update_frame(self):
        ret,image=self.cap.read()
        img=cv2.flip(image,1)
        self.display_img(img,True)
    #def display_img(self,img, window=True):
        
    def display_img(self,img,window=True):
        qormat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        outImg=QImage(img,img.shape[1], img.shape[0], img.strides[0],qformat)
        outImg=outImg.rgbSwapped()
        if window:
            self.cam_box.setPixmap(QPixmap.fromImage(outImg))
      
        
    def capture_img(self):
        flag,frame=self.cap.read()
        frame=cv2.flip(frame,1)
        base_dir=os.getcwd()
        path=os.path.join(base_dir, "test_imgs")

        if flag:
            QApplication.beep()
            name='img'+str(self.img_count)+'.jpg'
            cv2.imwrite(os.path.join(path,name), frame)
            self.img_count+=1
               
        selected=self.select_combo.currentText()
        print(selected)
        align_face(os.path.join(path,name))
        cwdir=os.getcwd()
        os.chdir("./STGAN/STGAN")
        system_input="python test.py --experiment_name 128 --dataroot data --img 202600 --test_atts "+selected+" --test_ints 2"
        os.system(system_input)
        os.chdir(cwdir)
        stgan_output="/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/output/128/sample_testing_multi/202600_['"+selected+"'].png"
        path_orig, path_result= divide_img(stgan_output, num_atts=1)
        #print(stgan_output)

        
    def window_change(self):
        select=self.select_combo.currentText()
        self.Window=Page2()
        self.Window.return_btn.clicked.connect(self.go_back)
        self.hide()
        self.Window.show()
        
            
    def go_back(self):
        self.show()
        self.Window.hide()

            
            
            
class Page2(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Page2,self).__init__(*args,**kwargs)
        self.setWindowTitle("Result")
        
        layout0=QVBoxLayout()
        layout1=QHBoxLayout()
        layout2=QVBoxLayout()
        layout3=QVBoxLayout()
        
        
        path_orig="/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/output/128/sample_testing_divided/202600_orig.jpg"
        path_result="/Users/alarazindancioglu/Desktop/Comp537/STGAN/STGAN/output/128/sample_testing_divided/202600_result.jpg"
   
        
        self.user_perf=QLabel()
        self.user_perf.setPixmap(QPixmap(path_orig))
        #Son değişim burası 
        #Neden burası self diğeri değil??? 
        self.user_perf.resize(200,200)
        self.user_perf.setAlignment(Qt.AlignCenter)
        layout2.addWidget(self.user_perf)
        layout2.addWidget(QLabel('Your performance', alignment=Qt.AlignCenter))
        

        correct_perf=QLabel()
        correct_perf.setPixmap(QPixmap(path_result))
        correct_perf.resize(200,200)
        correct_perf.setAlignment(Qt.AlignCenter)
        layout3.addWidget(correct_perf)
        layout3.addWidget(QLabel("Correct perfromance", alignment= Qt.AlignCenter))
        
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        
        layout0.addLayout(layout1)
        self.return_btn=QPushButton("Retry")
        layout0.addWidget(self.return_btn)
        
        
        widget=QWidget()
        widget.setLayout(layout0)
        self.setCentralWidget(widget)
        

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
        

        

    
    

