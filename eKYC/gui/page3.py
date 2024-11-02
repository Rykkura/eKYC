# import random
# import cv2
# import imutils
# import f_liveness_detection
# import questions
# from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
# from PyQt5.QtCore import QTimer, QRect
# from PyQt5.QtGui import QImage, QPixmap, QFont
# import sys
# import numpy as np
# from gui.utils import add_button
# # parameters
# COUNTER, TOTAL = 0, 0
# counter_ok_questions = 0
# counter_ok_consecutives = 0
# limit_consecutives = 3
# limit_questions = 3
# counter_try = 0
# limit_try = 50

# class LivenessDetectionApp(QWidget):
#     def __init__(self, camera, main_window):
#         super().__init__()

#         self.main_window = main_window
        
#         self.window_heigt = 800
#         self.window_width = 1600
        
#         self.setWindowTitle('Challenge response')
#         self.setGeometry(100, 100, self.window_width, self.window_heigt)
#         self.setFixedSize(self.window_width, self.window_heigt)

#         self.font = QFont()
#         self.font.setPointSize(13)
#         self.font.setFamily("Times New Roman")

#         self.label = QLabel(self)
#         self.label.setText('Verify your authenticity by completing the following challenges.')
#         self.label.move(520, 100)
#         self.label.setFont(self.font)

#         self.camera_label = QLabel(self)

#         self.camera = camera  # Open the default camera (usually the built-in webcam)
#         self.timer = QTimer(self)
        
#         # button 
#         self.next = add_button(self, "Exit", 1280, 700, 150, 50, exit)
#         self.back = add_button(self, "Back", 320, 700, 150, 50, self.back_switch_page)

#         # Variables to track state
#         self.index_question = random.randint(0, 4)
#         self.question = questions.question_bank(self.index_question)
#         self.challenge_res = None

#         # Initialize process label
#         self.process_label = QLabel(self)
#         self.process_label.move(730, 650)
#         self.process_label.setFont(self.font)
#         self.update_process_label(self.question)
    
#         self.is_delayed = False 
#         self.is_challenge_complete = False

    
#     def update_process_label(self, text=None):
#         if text is not None:
#             self.process_label.setText(text)
#         self.process_label.adjustSize()
#         self.process_label.show()
#     def rescale_image(self):
#         return 640, 480
#     def update_frame(self):
#         # Capture frame from camera
#         ret, frame = self.camera.read()
#         if ret:
#             frame = cv2.flip(frame, 1)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(image)
#             width, height = self.rescale_image()
#             self.camera_label.setGeometry(QRect(800 - width // 2, 150, width, height))
#             self.camera_label.setPixmap(pixmap)
#         if not ret:
#             return

#         global COUNTER, TOTAL, counter_ok_questions, counter_ok_consecutives, counter_try
#         if self.is_challenge_complete:  
#             return
#         # Update question if needed
#         if counter_ok_questions < limit_questions:
#             TOTAL_0 = TOTAL
#             out_model = f_liveness_detection.detect_liveness(frame, COUNTER, TOTAL_0)
#             TOTAL = out_model['total_blinks']
#             COUNTER = out_model['count_blinks_consecutives']
#             dif_blink = TOTAL - TOTAL_0
#             blinks_up = 1 if dif_blink > 0 else 0

#             self.challenge_res = questions.challenge_result(self.question, out_model, blinks_up)

#             if self.challenge_res == "pass":
#                 counter_ok_consecutives += 1
#                 if counter_ok_consecutives == limit_consecutives:
#                     counter_ok_questions += 1
#                     counter_ok_consecutives = 0
#                     counter_try = 0
#                     self.show_next_question_with_delay()
#                     self.update_process_label(self.question)

#             elif self.challenge_res == "fail":
#                 counter_try += 1
#                 self.update_process_label(self.question + " :")

            
#             if self.challenge_res == "pass":
#                 self.update_process_label(self.question + " : ok")

#         if counter_ok_questions == limit_questions:

#             self.update_process_label("LIVENESS SUCCESSFUL")
#             self.is_challenge_complete = True
#         elif counter_try >= limit_try:

#             self.update_process_label("LIVENESS FAIL")
#             self.is_challenge_complete = True

#     def show_next_question_with_delay(self):
#         """Show next question after a delay"""
#         self.is_delayed = True

#         QTimer.singleShot(2000, self.next_question)  

#     def next_question(self):
#         """Show the next question"""
#         self.is_delayed = False  
#         self.index_question = random.randint(0, 4)
#         self.question = questions.question_bank(self.index_question)
#         self.update_process_label(self.question)
#     def closeEvent(self, event):
#         self.cam.release()
#         event.accept()
#     def close_camera(self):
#         self.timer.stop()
#     def open_camera(self):
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(1000 // 120)  
#     def back_switch_page(self):
#         self.main_window.switch_page(1) 
    
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LivenessDetectionApp()
#     window.show()
#     sys.exit(app.exec_())



import random
import cv2
import imutils
import f_liveness_detection
import questions
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QImage, QPixmap, QFont
import sys
import numpy as np
from gui.utils import add_button

# parameters
COUNTER, TOTAL = 0, 0
counter_ok_questions = 0
counter_ok_consecutives = 0
limit_consecutives = 3
limit_questions = 3
counter_try = 0
limit_try = 50

class LivenessDetectionApp(QWidget):
    def __init__(self, camera, main_window):
        super().__init__()

        self.main_window = main_window
        
        self.window_heigt = 800
        self.window_width = 1600
        
        self.setWindowTitle('Challenge response')
        self.setGeometry(100, 100, self.window_width, self.window_heigt)
        self.setFixedSize(self.window_width, self.window_heigt)

        self.font = QFont()
        self.font.setPointSize(13)
        self.font.setFamily("Times New Roman")

        self.label = QLabel(self)
        self.label.setText('Verify your authenticity by completing the following challenges.')
        self.label.move(520, 100)
        self.label.setFont(self.font)

        self.camera_label = QLabel(self)

        self.camera = camera  # Open the default camera (usually the built-in webcam)
        self.timer = QTimer(self)
        
        # button 
        self.next = add_button(self, "Exit", 1280, 700, 150, 50, exit)
        self.back = add_button(self, "Back", 320, 700, 150, 50, self.back_switch_page)

        # Variables to track state
        self.available_questions = list(range(4))  # Assuming there are 5 questions (0 to 4)
        self.used_questions = []
        self.index_question = self.get_random_question(None)  # Initialize with no previous question
        self.question = questions.question_bank(self.index_question)
        self.challenge_res = None

        # Initialize process label
        self.process_label = QLabel(self)
        self.process_label.move(730, 650)
        self.process_label.setFont(self.font)
        self.update_process_label(self.question)
    
        self.is_delayed = False 
        self.is_challenge_complete = False

    
    def update_process_label(self, text=None):
        if text is not None:
            self.process_label.setText(text)
        self.process_label.adjustSize()
        self.process_label.show()

    def rescale_image(self):
        return 640, 480
    
    def get_random_question(self, prev_question):
        """Select a random question from available ones and move it to used list, ensuring no repeats."""
        if not self.available_questions:  # Reset when no more available questions
            self.available_questions = self.used_questions.copy()
            self.used_questions.clear()

        index_question = random.choice(self.available_questions)

        # Ensure the new question is not the same as the previous one
        while index_question == prev_question and len(self.available_questions) > 1:
            index_question = random.choice(self.available_questions)

        self.available_questions.remove(index_question)
        self.used_questions.append(index_question)
        return index_question
    
    def update_frame(self):
        # Capture frame from camera
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            width, height = self.rescale_image()
            self.camera_label.setGeometry(QRect(800 - width // 2, 150, width, height))
            self.camera_label.setPixmap(pixmap)
        if not ret:
            return

        global COUNTER, TOTAL, counter_ok_questions, counter_ok_consecutives, counter_try
        if self.is_delayed or self.is_challenge_complete:  
            return
        # Update question if needed
        if counter_ok_questions < limit_questions:
            TOTAL_0 = TOTAL
            out_model = f_liveness_detection.detect_liveness(frame, COUNTER, TOTAL_0)
            TOTAL = out_model['total_blinks']
            COUNTER = out_model['count_blinks_consecutives']
            dif_blink = TOTAL - TOTAL_0
            blinks_up = 1 if dif_blink > 0 else 0

            self.challenge_res = questions.challenge_result(self.question, out_model, blinks_up)

            if self.challenge_res == "pass":
                counter_ok_consecutives += 1
                if counter_ok_consecutives == limit_consecutives:
                    counter_ok_questions += 1
                    counter_ok_consecutives = 0
                    counter_try = 0
                    self.show_next_question_with_delay()
                    self.update_process_label(self.question)

            elif self.challenge_res == "fail":
                counter_try += 1
                self.update_process_label(self.question + " :")

            
            if self.challenge_res == "pass":
                self.update_process_label(self.question + " : ok")

        if counter_ok_questions == limit_questions:

            self.update_process_label("LIVENESS SUCCESSFUL")
            self.is_challenge_complete = True
        elif counter_try >= limit_try:

            self.update_process_label("LIVENESS FAIL")
            self.is_challenge_complete = True

    def show_next_question_with_delay(self):
        """Show next question after a delay"""
        self.is_delayed = True

        QTimer.singleShot(2000, self.next_question)  

    def next_question(self):
        """Show the next question"""
        self.is_delayed = False  
        prev_question = self.index_question  # Track the previous question
        self.index_question = self.get_random_question(prev_question)
        self.question = questions.question_bank(self.index_question)
        self.update_process_label(self.question)

    def closeEvent(self, event):
        self.cam.release()
        event.accept()
    
    def close_camera(self):
        self.timer.stop()
    
    def open_camera(self):
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 120)  
    
    def back_switch_page(self):
        self.main_window.switch_page(1) 
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LivenessDetectionApp()
    window.show()
    sys.exit(app.exec_())

