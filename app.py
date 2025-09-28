# app.py (vulnerable demo)
from flask import Flask, request, jsonify
import pickle
import yaml

app = Flask(__name__)

# 1) debug = True -> показывает stack trace / internal info
app.config['DEBUG'] = True

# 2) hardcoded secret
API_KEY = "FAKE_SECRET_API_KEY_12345"

# 3) load config with secrets from repo (config.yaml)
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

@app.route('/')
def index():
    return "Hello, world!"

@app.route('/cause_error')
def cause_error():
    # вызовет исключение и при debug=True вернёт стек трейсы с внутренней информацией
    raise RuntimeError("DB connection=postgresql://user:password@localhost:5432/dbname")

@app.route('/get_secret')
def get_secret():
    # возвращаем хардкод и конфиг -> уязвимость утечки секретов
    return jsonify({
        "api_key": API_KEY,
        "config_secret": cfg.get("secret")
    })

@app.route('/deserialize', methods=['POST'])
def deserialize():
    # Небезопасная десериализация: untrusted pickle !!!
    data = request.data
    obj = pickle.loads(data)   # ПОКАЗАТЕЛЬНО опасно — не используйте в prod
    return jsonify({"received": str(obj)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
