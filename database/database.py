from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Kích hoạt CORS

# Kết nối đến cơ sở dữ liệu PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        user='postgres',
        host='localhost',
        database='mobileappdb',
        password='020104',
        port=5432
    )
    return conn

# API đăng ký
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *', (username, password))
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
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[2] == password:  # user[2] là mật khẩu đã lưu
            return jsonify({'message': 'Đăng nhập thành công'}), 200
        else:
            return jsonify({'message': 'Tên đăng nhập hoặc mật khẩu không chính xác'}), 400

    except Exception as e:
        return jsonify({'message': 'Lỗi hệ thống', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
