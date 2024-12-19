from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import bcrypt
import jwt
import datetime

app = Flask(__name__)
CORS(app)  # Kích hoạt CORS

# Kết nối đến cơ sở dữ liệu PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        user='postgres',
        host='localhost',
        database='mobile',
        password='020104',
        port=5432
    )
    return conn

AES_KEY = b'HIjemN9zXkVGyd6bGFX9YLNyYQTtuRH9'
JWT_SECRET_KEY = 'b34102959c55904eed3521c62f4a4f6848f2db238338bf1894a8a38382419ecb02c7a8c3a16fd24a9b368db11da4259ca47f6dfde2b49a09cd776d542f633bfa137ad3c749d6aa6cdd1e84829de0dc060794ffcf2e130f993d56d92716b48d10eebe0f63b5f9be1a4e6ba9e052457b9399bd10e1f1dc9985e833ddc6ac12bbbc246ba74a43bc6d511b0fefabd82aa0582dcbc152be828cb3d87e3b42a673935ded6180ec9e9135fc83d5135eb7d7bb552702bbb0d8957c994c9165f6fe1ce6516e39e3bdb836d01ad6c2752cc325cd0249d4cb8d7b30d69f6fcb83ed311c290b1491a6eb44cde33a027c04242f7c52067ce24464aba0c1ab8d2d56416312fbea'
def encrypt_data(data):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB8(AES_KEY[:16]), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode()
def decrypt_data(encrypted_data):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB8(AES_KEY[:16]), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()
    return decrypted_data.decode()
# API đăng ký
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname')
    cccd = data.get('cccd')
    email = data.get('email')
    encrypted_fullname = encrypt_data(fullname)
    encrypted_cccd = encrypt_data(cccd)
    encrypted_email = encrypt_data(email)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    # password = hashed_password.decode('utf-8')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('INSERT INTO users (username, password, email, fullname, cccd) VALUES (%s, %s, %s, %s, %s) RETURNING *', (username, password, encrypted_email, encrypted_fullname, encrypted_cccd))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Đăng ký thành công', 'user': {'id': user[0], 'username': user[1]}}), 201

    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({'message': 'Tên đăng nhập đã tồn tại'}), 400
    except Exception as e:
        return jsonify({'message': 'Lỗi hệ thống', 'error': str(e)}), 500

# API đăng nhập
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Truy vấn để lấy mật khẩu mã hóa từ cơ sở dữ liệu
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[2] == password:  # user[2] là mật khẩu đã lưu
            # token = jwt.encode({
            #         'user_name': user[1],
            #         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            #     }, JWT_SECRET_KEY, algorithm='HS256')
            return jsonify({'message': 'Đăng nhập thành công'}), 200
        else:
            return jsonify({'message': 'Tên đăng nhập hoặc mật khẩu không chính xác'}), 400

    except Exception as e:
        return jsonify({'message': 'Lỗi hệ thống', 'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
