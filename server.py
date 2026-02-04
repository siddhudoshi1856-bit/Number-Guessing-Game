import bs4
import no_py_typed
from flask import Flask, request, jsonify, send_from_directory
import os
import json
import requests

app = Flask(__name__, static_folder='.', static_url_path='')
DATA_FILE = 'game_data.json'


def _load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _append_data(item):
    data = _load_data()
    data.append(item)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/save-data', methods=['POST'])
def save_data():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'missing payload'}), 400
    _append_data({'type': payload.get('type', 'unknown'), 'payload': payload.get('data', payload)})
    return jsonify({'status': 'ok'})


@app.route('/verify-token', methods=['POST'])
def verify_token():
    payload = request.get_json() or {}
    id_token = payload.get('id_token')
    if not id_token:
        return jsonify({'error': 'missing id_token'}), 400

    try:
        r = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': id_token}, timeout=5)
        if r.status_code != 200:
            return jsonify({'error': 'invalid_token', 'details': r.text}), 400
        info = r.json()

        # NOTE: in production, validate info['aud'] matches your CLIENT_ID
        profile = {
            'email': info.get('email'),
            'name': info.get('name'),
            'picture': info.get('picture')
        }
        _append_data({'type': 'signin', 'profile': profile, 'token_info': info})
        return jsonify({'status': 'ok', 'profile': profile})
    except Exception as e:
        return jsonify({'error': 'verification_failed', 'details': str(e)}), 500


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(_load_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)