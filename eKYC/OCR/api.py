import os
import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file
import re
from ocr import ocr, load_model
app = Flask(__name__)

# Configure the directory for saving uploaded files
app.config['UPLOAD_FOLDER'] = 'inference_results'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def secure_filename(filename):
    """
    Converts a filename to a secure format by removing unwanted characters.
    Only allows letters, numbers, underscores, hyphens, and dots.
    """
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename

class Transfer:

    @staticmethod
    def filepath_to_array(file_content):
        return cv2.imread(file_content)

    @staticmethod
    def base64_to_array(base64_img):
        img = base64.b64decode(base64_img)
        image_data = np.frombuffer(img, np.uint8)
        return cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    @staticmethod
    def bytes_to_array(content):
        image_data = np.frombuffer(content, np.uint8)
        return cv2.imdecode(image_data, cv2.IMREAD_COLOR)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to PaddleOCR API. Use /docs for API documentation."})

@app.route("/ocr/dict", methods=["POST"])
def ocr_dict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)
    
    # Process the image
    array = Transfer.bytes_to_array(file.read())
    return ocr(array)

@app.route("/ocr/file", methods=["POST"])
def ocr_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)
    
    # Process the image
    array = Transfer.bytes_to_array(file.read())
    # Call the ocr function (you should implement this function)
    result_file_path = ocr(array, download_filename=file.filename)  # Ensure ocr() returns a file path
    
    return result_file_path

@app.route("/ocr/base64", methods=["POST"])
def ocr_base64():
    data = request.get_json()
    base64_img = data.get('base64')
    
    if base64_img is None:
        return jsonify({"error": "Base64 image data is required."}), 400
    
    array = Transfer.base64_to_array(base64_img)
    return ocr(array)  # Ensure ocr() is defined

if __name__ == '__main__':
    LOG_PATH = os.path.join(os.path.dirname(__file__), 'paddle_ocr_api.log')
    host, port = '0.0.0.0', 8000
    # Set up logging as needed, e.g., using the logging module
    print(f'Binding on {host}:{port}, log path is {LOG_PATH}')
    load_model()  # Ensure this function is defined
    app.run(host=host, port=port)
