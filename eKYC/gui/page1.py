# from PyQt5.QtCore import QPoint, QRect, Qt, QTimer
# from PyQt5.QtGui import QFont, QImage, QPainter, QPen, QPixmap
# from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QHBoxLayout,
#                              QLabel, QMainWindow, QPushButton, QStackedWidget,
#                              QVBoxLayout, QWidget)

# import cv2 as cv
# from .utils import *
# from OCR.predict import run_ocr


# class IDCardPhoto(QWidget):
#     def __init__(self, main_window):
#         super().__init__()

#         self.main_window = main_window

#         self.window_heigt = 800
#         self.window_width = 1600
                
#         # Thiết lập tiêu đề và kích thước của cửa sổ
#         self.setWindowTitle('Choose ID Card Photo')
#         self.setGeometry(100, 100, self.window_width, self.window_heigt)
#         self.setFixedSize(self.window_width, self.window_heigt)
        
#         self.font = QFont()
#         self.font.setPointSize(13)
#         self.font.setFamily("Times New Roman")

#         self.label = QLabel(self)
#         self.label.setText('Please select the front side of your national identity card.')
#         self.label.move(550, 100)
#         self.label.setFont(self.font)
        
#         self.exit_button = add_button(self, "Exit", 800, 700, 150, 50, exit)
    
#         self.select_image_button = add_button(self, "Select ID Card", 320, 700, 150, 50, self.selectImage)
#         self.next = add_button(self, "Next", 1280, 700, 150, 50, self.switch_page, disabled = True)
#         self.in_image = QLabel(self)
        
#         self.img_path = None
    
#     def switch_page(self):
#         self.main_window.switch_page(1)     
        
#     def rescale_image(self, width, height):
#         return int(width * 400 / height), 400

#     def selectImage(self):
#         # Hiển thị hộp thoại chọn tệp ảnh và lấy tên tệp ảnh được chọn
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)')
        
#         if file_name:
#             self.img_path = file_name
#             # Tải ảnh từ tệp và hiển thị nó trên QLabel
#             pixmap = QPixmap(file_name)
#             img = cv.imread(file_name)
#             width, height = self.rescale_image(img.shape[1], img.shape[0])
#             self.in_image.setGeometry(QRect(800 - width //2 , 150, width, height))
#             self.in_image.setPixmap(pixmap.scaled(width, height))  
#             self.in_image.show()  
#             self.next.setDisabled(False)

#     def clear_window(self):
#         self.in_image.hide()






import random
import requests  # Thêm thư viện requests
import cv2 as cv
from PyQt5.QtCore import QPoint, QRect, Qt, QTimer
from PyQt5.QtGui import QFont, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QHBoxLayout,
                             QLabel, QMainWindow, QPushButton, QStackedWidget,
                             QVBoxLayout, QWidget)
from .utils import add_button  # Đảm bảo bạn đã có hàm add_button

class IDCardPhoto(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.window_heigt = 800
        self.window_width = 1600
                
        # Thiết lập tiêu đề và kích thước của cửa sổ
        self.setWindowTitle('Choose ID Card Photo')
        self.setGeometry(100, 100, self.window_width, self.window_heigt)
        self.setFixedSize(self.window_width, self.window_heigt)
        
        self.font = QFont()
        self.font.setPointSize(13)
        self.font.setFamily("Times New Roman")

        self.label = QLabel(self)
        self.label.setText('Please select the front side of your national identity card.')
        self.label.move(550, 100)
        self.label.setFont(self.font)
        
        self.exit_button = add_button(self, "Exit", 800, 700, 150, 50, exit)
    
        self.select_image_button = add_button(self, "Select ID Card", 320, 700, 150, 50, self.selectImage)
        self.next = add_button(self, "Next", 1280, 700, 150, 50, self.switch_page, disabled=True)
        self.in_image = QLabel(self)
        
        self.img_path = None
    
    def switch_page(self):
        self.main_window.switch_page(1)     
        
    def rescale_image(self, width, height):
        return int(width * 400 / height), 400

    def selectImage(self):
        # Hiển thị hộp thoại chọn tệp ảnh và lấy tên tệp ảnh được chọn
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)')
        
        if file_name:
            self.img_path = file_name
            # Tải ảnh từ tệp và hiển thị nó trên QLabel
            pixmap = QPixmap(file_name)
            img = cv.imread(file_name)
            width, height = self.rescale_image(img.shape[1], img.shape[0])
            self.in_image.setGeometry(QRect(800 - width // 2, 150, width, height))
            self.in_image.setPixmap(pixmap.scaled(width, height))  
            self.in_image.show()  
            self.next.setDisabled(False)

            # Gửi ảnh lên API và nhận lại đường dẫn đến file ảnh kết quả
            result_image_path = self.send_image_to_api(file_name)
            if result_image_path:
                self.show_result_image(result_image_path)

    def send_image_to_api(self, image_path):
        """Gửi ảnh đến API và trả về đường dẫn đến ảnh kết quả."""
        url = "http://127.0.0.1:8000/ocr/file"  # Thay đổi đường dẫn API của bạn
        with open(image_path, 'rb') as f:
            files = {'file': f}
            try:
                response = requests.post(url, files=files)
                response.raise_for_status()  # Kiểm tra xem có lỗi không
                return response.json().get('result_image_path')  # Thay đổi tùy theo cấu trúc trả về của API
            except requests.RequestException as e:
                print(f"Error sending image to API: {e}")
                return None

    def show_result_image(self, result_image_path):
        """Hiển thị ảnh kết quả từ API."""
        pixmap = QPixmap(result_image_path)
        # Rescale ảnh kết quả nếu cần
        width, height = self.rescale_image(pixmap.width(), pixmap.height())
        self.in_image.setGeometry(QRect(800 - width // 2, 150, width, height))
        self.in_image.setPixmap(pixmap.scaled(width, height))
        self.in_image.show()

    def clear_window(self):
        self.in_image.hide()
