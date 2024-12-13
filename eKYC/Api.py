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
import os
from werkzeug.utils import secure_filename
import jwt
from functools import wraps
# Khởi tạo Flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
detector = MTCNN()
load_model()
# Các biến toàn cục cho liveness detection
COUNTER = 0
TOTAL = 0
JWT_SECRET_KEY = 'b34102959c55904eed3521c62f4a4f6848f2db238338bf1894a8a38382419ecb02c7a8c3a16fd24a9b368db11da4259ca47f6dfde2b49a09cd776d542f633bfa137ad3c749d6aa6cdd1e84829de0dc060794ffcf2e130f993d56d92716b48d10eebe0f63b5f9be1a4e6ba9e052457b9399bd10e1f1dc9985e833ddc6ac12bbbc246ba74a43bc6d511b0fefabd82aa0582dcbc152be828cb3d87e3b42a673935ded6180ec9e9135fc83d5135eb7d7bb552702bbb0d8957c994c9165f6fe1ce6516e39e3bdb836d01ad6c2752cc325cd0249d4cb8d7b30d69f6fcb83ed311c290b1491a6eb44cde33a027c04242f7c52067ce24464aba0c1ab8d2d56416312fbea'

# def token_required(f):
#     """Middleware kiểm tra JWT token"""
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         # Lấy token từ header Authorization
#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization'].split(" ")[1]  # Dạng: "Bearer <token>"

#         if not token:
#             return jsonify({"error": "Token is missing"}), 401

#         try:
#             # Giải mã token
#             data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
#             request.user = data  # Lưu thông tin user vào request
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token has expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"error": "Invalid token"}), 401

#         return f(*args, **kwargs)
#     return decorated
# Giới hạn số lần thử
limit_try = 5
limit_consecutives = 3
counter_ok_consecutives = 0
counter_ok_questions = 0

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Giới hạn file 50MB
# Tạo thư mục uploads nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    """Kiểm tra định dạng file được phép"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
# @token_required
def upload_video():
    # Kiểm tra xem request có chứa file không
    if 'video' not in request.files:
        return jsonify({'error': 'Không có file video'}), 400
    file = request.files['video']
    question = request.form.get('question')
    # Kiểm tra tên file
    if file.filename == '':
        return jsonify({'error': 'Không có file được chọn'}), 400
    # Kiểm tra định dạng file
    if file and allowed_file(file.filename):
        # Bảo vệ tên file
        filename = secure_filename(file.filename)
        # Tạo đường dẫn lưu file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            # Đường dẫn tệp video và câu hỏi được nhận trực tiếp từ hệ thống
            video_path = "./uploads/video.mp4"  # Thay bằng đường dẫn thực tế

            # Kiểm tra xem video có tồn tại không
            if not os.path.exists(video_path):
                return jsonify({"error": "Video file not found"}), 404

            # Mở video để xử lý
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return jsonify({"error": "Failed to open video"}), 500

            result = "fail"  # Mặc định kết quả là 'fail'
            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # Kết thúc video

                # Gọi hàm detect_liveness để xử lý từng khung hình
                result = detect_liveness(frame, question)
                if result == "pass":
                    break  # Nếu đạt yêu cầu, dừng xử lý

            cap.release()

            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
# Hàm xử lý yêu cầu liveness detection
def detect_liveness(im, question):
    global COUNTER, TOTAL, counter_ok_consecutives, counter_ok_questions
    
    
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
@app.route('/liveness_detection', methods=['POST'])
# @token_required
def liveness_detection():
    global COUNTER, TOTAL
    
    try:
        data = request.get_json()
        if not data or 'image' not in data or 'question' not in data:
            return jsonify({"error": "Missing image or question"}), 400
        
        # Nhận hình ảnh (base64) và câu hỏi từ client
        question = data['question']
        image_base64 = data['image']
        
        im = base64_to_array(image_base64)
        
        result = detect_liveness(im, question)
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/detect_faces', methods=['POST'])
# @token_required
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
        face2 = '/workspace/eKYC/eKYC/FaceNet/img/trung1.JPG'
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
    start_index = transcriptions.index("Card") + 3
    end_index = transcriptions.index("Họ")
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
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    