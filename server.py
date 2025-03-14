from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище сессий (имитация базы данных)
SESSIONS = {}

@app.route('/')
def home():
    return jsonify({"message": "API is running"}), 200

# 📌 Логин: возвращает session cookie
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

# 📌 Проверка сессии
@app.route('/check-session', methods=['GET'])
def check_session():
    session_token = request.args.get('session')

    if session_token in SESSIONS:
        return jsonify({"message": "Session is valid"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

# 📌 Запрос на сбор наград (game/harvest)
@app.route('/game/harvest', methods=['GET'])
def harvest():
    session_token = request.headers.get('Authorization', '').replace("Bearer ", "")

    if session_token not in SESSIONS:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "Harvest successful", "reward": "50 coins"}), 200

# 📌 Запрос на список квестов (quest/all)
@app.route('/quest/all', methods=['GET'])
def get_quests():
    session_token = request.headers.get('Authorization', '').replace("Bearer ", "")

    if session_token not in SESSIONS:
        return jsonify({"error": "Unauthorized"}), 401

    quests = [
        {"id": 1, "name": "Complete daily challenge", "status": "OPENED"},
        {"id": 2, "name": "Win 3 coin flips", "status": "COMPLETED"}
    ]
    return jsonify({"quests": quests}), 200

# 📌 Запрос на статистику пользователя
@app.route('/statistic/user', methods=['GET'])
def user_stat():
    session_token = request.headers.get('Authorization', '').replace("Bearer ", "")

    if session_token not in SESSIONS:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "info": {"telegram": {"username": "test_user", "id": "123456"}},
        "statistic": {"tonBalance": "0.5", "terminalBalance": 100},
        "packStatistic": {},
        "referralStatistic": {}
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
