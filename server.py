from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Храним сессии в памяти (лучше использовать базу данных)
sessions = {}

@app.route('/login', methods=['POST'])
def login():
    """Создаёт session cookie при логине"""
    username = request.json.get("username")
    password = request.json.get("password")

    if username == "admin" and password == "1234":
        session_id = secrets.token_hex(32)  # Генерируем случайный session cookie
        sessions[username] = session_id
        return jsonify({"session": session_id})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/check-session', methods=['GET'])
def check_session():
    """Проверяет session cookie"""
    session_id = request.args.get("session")
    if session_id in sessions.values():
        return jsonify({"message": "Session is valid"})
    else:
        return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

