import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import imutils
import base64
import random 
import cv2
import f_liveness_detection
import questions
from mtcnn import MTCNN
from io import BytesIO
from PIL import Image
from flask_socketio import SocketIO, emit
# from mtcnn import MTCNN
from FaceNet.predict import compare_images
from OCR.ocr import ocr, load_model


# Khởi tạo Flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
detector = MTCNN()
load_model()
# Các biến toàn cục cho liveness detection
COUNTER = 0
TOTAL = 0

# Giới hạn số lần thử
limit_try = 5
limit_consecutives = 3
counter_ok_consecutives = 0
counter_ok_questions = 0

# Hàm xử lý yêu cầu liveness detection
def detect_liveness(im, question):
    global COUNTER, TOTAL, counter_ok_consecutives, counter_ok_questions
    
    # Các bước xử lý ảnh tương tự như trong mã nguồn
    im = imutils.resize(im, width=720)
    im = cv2.flip(im, 1)
    
    TOTAL_0 = TOTAL
    out_model = f_liveness_detection.detect_liveness(im, COUNTER, TOTAL_0)
    TOTAL = out_model['total_blinks']
    COUNTER = out_model['count_blinks_consecutives']
    dif_blink = TOTAL - TOTAL_0
    blinks_up = 1 if dif_blink > 0 else 0
    
    # Kiểm tra thử thách
    challenge_res = questions.challenge_result(question, out_model, blinks_up)
    
    if challenge_res == "pass":
        return "pass"
    elif challenge_res == "fail":
        return "fail"
    else:
        return "retry"

def crop_face(image):
    """Sử dụng MTCNN để phát hiện và cắt khuôn mặt từ ảnh."""
    detections = detector.detect_faces(image)
    if len(detections) == 0:
        return None
    
    x, y, w, h = detections[0]['box']
    cropped_face = image[y:y+h, x:x+w]
    return cropped_face

def base64_to_array(base64_img):
        img = base64.b64decode(base64_img)
        image_data = np.frombuffer(img, np.uint8)
        return cv2.imdecode(image_data, cv2.IMREAD_COLOR)
# API endpoint để kiểm tra liveness
@app.route('/')
def index():
    return "WebSocket server is running!"

# WebSocket event to handle the image upload
@socketio.on('upload_image')
def handle_image(data):
    image_data = data['image']  # Get the base64 image data
    image = base64.b64decode(image_data)  # Decode the image
    img = Image.open(BytesIO(image))  # Convert to an image object
    img.save('uploaded_image.jpg')  # Save the image to a file
    print("Image uploaded and saved successfully!")
    emit('response', {'message': 'Image received successfully!'})

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    try:
        # Nhận dữ liệu ảnh
        data = request.get_json()
        if not data or 'image1' not in data:
            return jsonify({"error": "Missing image or question"}), 400
        image_base64 = data['image1']
        img1 = base64_to_array(image_base64)
        face1 = cv2.flip(img1, 1)
        cv2.imwrite("face1.jpg", face1)

        # Cắt khuôn mặt
        img_cccd = cv2.imread('cccd.jpg')
        face_cccd = crop_face(img_cccd)
        cv2.imwrite("face_cccd.jpg", face_cccd)
        
    
        face1 = 'face1.jpg'
        face2 = 'face_cccd.jpg'
        if face1 is None or face2 is None:
            return jsonify({"error": "Không tìm thấy khuôn mặt trong một trong hai ảnh"}), 400
        result = compare_images(face1, face2)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/ocr', methods=['POST'])
def ocr_base64():
    data = request.get_json()
    image_base64 = data['image1']

    array = base64_to_array(image_base64)
    cv2.imwrite("cccd.jpg", array)
    
    result = ocr(array)
    transcriptions = [item["transcription"] for item in result]

    # Ten
    start_index = transcriptions.index("Full") + 2
    end_index = transcriptions.index("Ngày")
    name_elements = transcriptions[start_index:end_index]
    ho_ten = [" ".join(name_elements)]

    # So CCCD
    start_index = transcriptions.index("Card") + 1
    end_index = transcriptions.index("Số")
    CCCD = transcriptions[start_index:end_index]
    
    # Ngày sinh
    start_index = transcriptions.index("Date") + 3
    end_index = transcriptions.index("Date") + 4 
    ngay_sinh = transcriptions[start_index:end_index]
    #Que quán
    start_index = transcriptions.index("origin") + 1
    end_index = transcriptions.index("Nơi")
    que_quan = transcriptions[start_index:end_index]
    que_quan = [" ".join(que_quan)]
    return jsonify({ "CCCD": CCCD,  "ho_ten": ho_ten, "ngay_sinh": ngay_sinh, "que_quan": que_quan})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    