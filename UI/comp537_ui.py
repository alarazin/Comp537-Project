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

from test_py_import import modif

"""
try:
    os.remove(imgpath)
except:
    pass

"""

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.setWindowTitle("Cam Trial")
        general_layout=QStackedLayout()
        page1_layout= QHBoxLayout() 
        page1_1_layout=QVBoxLayout()
        
        page2=QLabel("Hello")
        
        select_combo=QComboBox()
        select_combo.addItems(["Select","Happy", "Sad", "Neutral"])
        select_combo.currentIndexChanged.connect(self.start_cam)
        #select_combo.currentIndexChanged.connect(self.display_img)
        self.cap=None
        
        page1_layout.addWidget(select_combo)

        self.cam_box=QLabel()
        #cam_box.setPixmap(QPixmap("cat.jpeg"))
        page1_1_layout.addWidget(self.cam_box)
        
        capture_button=QPushButton("Capture")
        capture_button.clicked.connect(self.capture_img)
        capture_button.clicked.connect(self.window_change)
        page1_1_layout.addWidget(capture_button)
        
        
        
        page1_layout.addLayout(page1_1_layout)
        
        #general_layout.addLayout(page1_layout)
        #general_layout.addChildLayout(page1_layout)
        #general_layout.addWidget(page2)
        #general_layout.setCurrentIndex(0)
        
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
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
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
    
            
    
# =============================================================================
#     
# =============================================================================
    
        
    def capture_img(self):
        flag,frame=self.cap.read()
        frame=cv2.flip(frame,1)
        path = '/Users/alarazindancioglu/Desktop/pyqt5_tutorial/comp537/test_imgs/'
        if flag:
            QApplication.beep()
            name='img'+str(self.img_count)+'.jpg'
            self.page2=Page2()           
            #self.page2.user_perf.setPixmap(QPixmap(QImage(frame)))        
            cv2.imwrite(path+name, frame)
            self.page2.user_perf.setPixmap(QPixmap(path+name))
            #self.img_count+=1
        
            
# =============================================================================
#         
# =============================================================================
        
        
        
    def window_change(self):
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
        
        self.user_perf=QLabel()
        self.user_perf.setPixmap(QPixmap("test_imgs/img0.jpg"))
        layout2.addWidget(self.user_perf)
        layout2.addWidget(QLabel('Your performance', alignment=Qt.AlignCenter))
        
        
        path=modif("test_imgs/")
        correct_perf=QLabel()
        correct_perf.setPixmap(QPixmap(path))
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
        

        

    
    

