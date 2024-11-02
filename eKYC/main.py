import sys
import torch
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget



from gui.page1 import *
from gui.page2 import *
from gui.page3 import *
from gui.utils import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  

        self.window_heigt = 800
        self.window_width = 1600
        self.setWindowTitle("eKYC GUI")
        self.setGeometry(100, 100, self.window_width, self.window_heigt)
        self.setFixedSize(self.window_width, self.window_heigt)
        
        

        # camera
        self.camera = cv.VideoCapture(0)

        # stack widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.first_page = IDCardPhoto(main_window = self)
        self.second_page = VerificationWindow(camera = self.camera, main_window = self)
        self.third_page = LivenessDetectionApp(camera=self.camera, main_window=self)

        self.stacked_widget.addWidget(self.first_page)
        self.stacked_widget.addWidget(self.second_page)
        self.stacked_widget.addWidget(self.third_page)
               

    def switch_page(self, index):
        if index == 0:
            self.first_page.clear_window()
            self.second_page.close_camera()
            self.third_page.close_camera()
        
        elif index == 1:
            self.second_page.clear_window()
            self.second_page.open_camera()
            self.third_page.close_camera()
        
        elif index == 2:
            # self.third_page.clear_window()
            self.third_page.open_camera()
            self.second_page.close_camera()
            
        self.stacked_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
