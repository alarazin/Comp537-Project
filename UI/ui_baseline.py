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





class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.setWindowTitle("Cam Trial")
        general_layout=QStackedLayout()
        page1_layout= QHBoxLayout() 
        page1_1_layout=QVBoxLayout()
        
        page2=QLabel("Hello")
        
        select_combo=QComboBox()
        select_combo.addItems(["Happy", "Sad", "Neutral"])
        
        page1_layout.addWidget(select_combo)

        cam_box=QLabel()
        cam_box.setPixmap(QPixmap("cat.jpeg"))
        page1_1_layout.addWidget(cam_box)
        
        capture_button=QPushButton("Capture")
        capture_button.clicked.connect(self.window_change)
        page1_1_layout.addWidget(capture_button)
        
        
        page1_layout.addLayout(page1_1_layout)
        
        #general_layout.addLayout(page1_layout)
        #general_layout.addChildLayout(page1_layout)
        #general_layout.addWidget(page2)
        #general_layout.setCurrentIndex(0)
        
        widget=QWidget()
        widget.setLayout(page1_layout)
        self.setCentralWidget(widget)
        
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
        
        user_perf=QLabel()
        user_perf.setPixmap(QPixmap("cat.jpeg"))
        layout2.addWidget(user_perf)
        layout2.addWidget(QLabel('Your performance', alignment=Qt.AlignCenter))
        
        
        
        correct_perf=QLabel()
        correct_perf.setPixmap(QPixmap("dog.jpeg"))
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
        

        

    
    

