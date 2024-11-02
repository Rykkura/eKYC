from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import imutils
import f_liveness_detection
import questions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class LivenessDetectionSession:
    def __init__(self):
        self.counter = 0
        self.total = 0
        self.counter_ok_questions = 0
        self.counter_ok_consecutives = 0
        self.counter_try = 0
        self.current_question_index = None
        self.limit_consecutives = 3
        self.limit_questions = 3
        self.limit_try = 50
        self.generate_new_question()
    
    def generate_new_question(self):
        self.current_question_index = np.random.randint(0, 4)
        return questions.question_bank(self.current_question_index)
    
    def process_frame(self, frame):
        # Xử lý frame
        frame = imutils.resize(frame, width=720)
        
        # Phát hiện khuôn mặt và tính toán các metrics
        out_model = f_liveness_detection.detect_liveness(frame, self.counter, self.total)
        
        prev_total = self.total
        self.total = out_model['total_blinks']
        self.counter = out_model['count_blinks_consecutives']
        
        dif_blink = self.total - prev_total
        blinks_up = 1 if dif_blink > 0 else 0
        
        # Kiểm tra kết quả thử thách
        current_question = questions.question_bank(self.current_question_index)
        challenge_res = questions.challenge_result(current_question, out_model, blinks_up)
        
        response = {
            'status': 'processing',
            'challenge_result': challenge_res,
            'current_question': current_question,
            'counter_ok_questions': self.counter_ok_questions,
            'counter_try': self.counter_try
        }
        
        if challenge_res == "pass":
            self.counter_ok_consecutives += 1
            if self.counter_ok_consecutives == self.limit_consecutives:
                self.counter_ok_questions += 1
                self.counter_try = 0
                self.counter_ok_consecutives = 0
                if self.counter_ok_questions < self.limit_questions:
                    response['current_question'] = self.generate_new_question()
                else:
                    response['status'] = 'success'
                    response['message'] = 'LIVENESS SUCCESSFUL'
        elif challenge_res == "fail":
            self.counter_try += 1
            if self.counter_try >= self.limit_try:
                response['status'] = 'fail'
                response['message'] = 'LIVENESS FAILED'
        
        return response

# Dictionary để lưu trữ các phiên
sessions = {}

@app.route('/api/start-session', methods=['POST'])
def start_session():
    session_id = base64.b64encode(os.urandom(24)).decode('utf-8')
    sessions[session_id] = LivenessDetectionSession()
    return jsonify({
        'session_id': session_id,
        'current_question': sessions[session_id].generate_new_question()
    })

@app.route('/api/process-frame', methods=['POST'])
def process_frame():
    data = request.json
    session_id = data.get('session_id')
    frame_data = data.get('frame')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    if not frame_data:
        return jsonify({'error': 'No frame data provided'}), 400
    
    # Chuyển đổi base64 frame thành numpy array
    frame_bytes = base64.b64decode(frame_data.split(',')[1])
    frame_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)
    
    # Xử lý frame
    result = sessions[session_id].process_frame(frame)
    
    # Nếu phiên đã hoàn thành (thành công hoặc thất bại), xóa phiên
    if result['status'] in ['success', 'fail']:
        del sessions[session_id]
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)