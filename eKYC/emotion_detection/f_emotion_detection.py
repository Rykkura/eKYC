import config as cfg
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

class predict_emotions():
    def __init__(self):
        
        self.model = load_model(cfg.path_model)

    def preprocess_img(self,face_image,rgb=True,w=48,h=48):
        face_image = cv2.resize(face_image, (w,h))
        if rgb == False:
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = face_image.astype("float") / 255.0
        face_image= img_to_array(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        return face_image

    def get_emotion(self,img,boxes_face):
        emotions = []
        if len(boxes_face)!=0:
            for box in boxes_face:
                y0,x0,y1,x1 = box
                face_image = img[x0:x1,y0:y1]
               
                face_image = self.preprocess_img(face_image ,cfg.rgb, cfg.w, cfg.h)
               
                prediction = self.model.predict(face_image)
                emotion = cfg.labels[prediction.argmax()]
                emotions.append(emotion)
        else:
            emotions = []
            boxes_face = []
        return boxes_face,emotions

## -----------Pytorch-----------
# import config as cfg
# import cv2
# import numpy as np
# import torch
# from torchvision import transforms
# from .vgg import VGG

# class PredictEmotions():
#     def __init__(self):
#         # Tải model PyTorch
#         trained_model = torch.load("emotion_detection/Modelos/model_state.pth.tar")
#         self.model = VGG("VGG19")
#         self.model.load_state_dict(trained_model["model_weights"])
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         # self.model.to(device)
#         self.model.eval()  # Chuyển model sang chế độ đánh giá

#         # Định nghĩa các phép biến đổi cho dữ liệu đầu vào
#         self.transform = transforms.Compose([
#             transforms.ToPILImage(),
#             transforms.Resize((cfg.w, cfg.h)),
#             transforms.ToTensor(),
#             transforms.Normalize((0.5,), (0.5,))  # Giả sử ảnh có 1 kênh (grayscale)
#         ])

#     def preprocess_img(self, face_image, rgb=True):
#         if not rgb:
#             face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
#         face_image = self.transform(face_image)
#         face_image = face_image.unsqueeze(0)  # Thêm chiều cho batch size
#         return face_image

#     def get_emotion(self, img, boxes_face):
#         emotions = []
#         if len(boxes_face) != 0:
#             for box in boxes_face:
#                 y0, x0, y1, x1 = box
#                 face_image = img[x0:x1, y0:y1]
#                 # Tiền xử lý dữ liệu
#                 face_image = self.preprocess_img(face_image, cfg.rgb)
#                 # Dự đoán
#                 with torch.no_grad():  # Tắt gradient khi dự đoán
#                     prediction = self.model(face_image)
#                 emotion = cfg.labels[torch.argmax(prediction).item()]
#                 emotions.append(emotion)
#         else:
#             emotions = []
#             boxes_face = []
#         return boxes_face, emotions

