from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище сессий (имитация базы данных)
SESSIONS = {}

@app.route('/')
def home():
    return jsonify({"message": "API is running"}), 200

# Логин: возвращает session cookie
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == "admin" and password == "1234":
        session_token = "9d719cd7d1012973e5fa2d527a4210d9cedb32571245fb6efc0782646e5b77ca"
        SESSIONS[session_token] = {"user": username}
        return jsonify({"session": session_token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Проверка сессии
@app.route('/check-session', methods=['GET'])
def check_session():
    session_token = request.args.get('session')
    if session_token in SESSIONS:
        return jsonify({"message": "Session is valid"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

# Сбор наград
@app.route('/game/harvest', methods=['GET'])
def harvest():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        session_token = auth_header.split(' ')[1]
        if session_token in SESSIONS:
            return jsonify({"message": "Harvest successful", "reward": "50 coins"}), 200
    return jsonify({"error": "Unauthorized"}), 401

# Получение всех квестов
@app.route('/quest/all', methods=['GET'])
def get_quests():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        session_token = auth_header.split(' ')[1]
        if session_token in SESSIONS:
            quests = [
                {"id": 1, "name": "Complete daily challenge", "status": "OPENED"},
                {"id": 2, "name": "Win 3 coin flips", "status": "COMPLETED"}
            ]
            return jsonify({"quests": quests}), 200
    return jsonify({"error": "Unauthorized"}), 401

# Статистика игры "Подбрось монетку"
@app.route('/game/coinflip/stats', methods=['GET'])
def get_coinflip_stats():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        session_token = auth_header.split(' ')[1]
        if session_token in SESSIONS:
            stats = {
                "games_left": 3,
                "flip_history": [
                    {"sessionId": 1, "side": "HEADS"},
                    {"sessionId": 2, "side": "TAILS"}
                ],
                "min_bet": 50,
                "max_bet": 5000
            }
            return jsonify(stats), 200
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
