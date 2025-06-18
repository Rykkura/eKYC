This repository is about eKYC, including face recognition, liveness detection, and OCR for ID cards. It provides a security-focused pipeline for banking apps in particular, and for high-security applications in general. The repository also includes a simple demo built with React Native showcasing a money transfer application integrated with eKYC.


# Installation
Clone this repo here:
```Shell
git clone https://github.com/Rykkura/eKYC.git
```
Create a conda virtual environment
```Shell
conda create -n paddleocr python=3.8
conda activate paddleocr
```
dlib dependence
```Shell
apt-get update
apt-get install build-essential cmake
apt-get install libopenblas-dev liblapack-dev 
apt-get install libx11-dev libgtk-3-dev
apt-get install python3 python3-dev python3-pip
```
Requirements
```Shell
pip install -r requirements.txt
```
# eKYC
- you can get pretrain model for face recognition, liveness detection and OCR here: https://drive.google.com/file/d/1eaDJj5DOBQEjiCX9a9uWBijSGS15sXkk/view?usp=drive_link
  - move **model_data** folder to your_path/eKYC/FaceNet/
  - move **Modelos** to your_path/eKYC/emotion_detection/
  - move **model_landmarks** to your_path/eKYC/blink_detection/
  - move **det_EAST** and **rec_SRN** to your_path/eKYC/OCR/
# Demo app
- This demo run in expo go in ios with sdk version 53.0.0
- Run this script:
```Shell
cd my_app
npm install 
npx expo start
```
- you will get a QR code in your terminal, scan this with your camera app and enjoy your testing
