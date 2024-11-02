import os
import cv2
import re
from ocr import ocr, load_model

# Ensure the directory for saving results exists
UPLOAD_FOLDER = 'inference_results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def secure_filename(filename):
    """
    Converts a filename to a secure format by removing unwanted characters.
    Only allows letters, numbers, underscores, hyphens, and dots.
    """
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename

class Transfer:

    @staticmethod
    def filepath_to_array(file_path):
        return cv2.imread(file_path)

def process_image_from_file(file_path):
    """
    Process the image from a local file path and return the OCR result.
    """
    # Load the image from the given file path
    array = Transfer.filepath_to_array(file_path)
    
    # Check if the image was loaded successfully
    if array is None:
        return {"error": f"Could not load image from {file_path}"}
    
    # Process the image using the OCR function
    result = ocr(array, download_filename='/result.jpg')
    
    return result

def run_ocr(file_path):
    load_model()  # Ensure this function is defined
    result = process_image_from_file(file_path)
    print("OCR Result:", result)

if __name__ == '__main__':
    # For testing or running directly
    file_path = input("Please enter the path to the image file: ")
    run_ocr(file_path)
