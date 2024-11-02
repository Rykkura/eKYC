from PIL import Image
from FaceNet.facenet import Facenet

def compare_images(image_path_1, image_path_2):
    model = Facenet()
    
    try:
        image_1 = Image.open(image_path_1)
    except Exception as e:
        print(f'Error opening image 1: {e}')
        return None

    try:
        image_2 = Image.open(image_path_2)
    except Exception as e:
        print(f'Error opening image 2: {e}')
        return None
    
    probability = model.detect_image(image_1, image_2)
    print(probability)
    if probability > 0.5:
        return 'Same person'
    else:
        return 'Different person'

if __name__ == "__main__":
    # Mã này có thể dùng để thử nghiệm hàm
    image_1_path = input('Input image_1 filename: ')
    image_2_path = input('Input image_2 filename: ')
    
    result = compare_images(image_1_path, image_2_path)
    if result:
        print(result)
        
