from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # allow requests from the Express frontend (different port)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

TOOLS = [
    {'id': 'docker', 'name': 'Docker', 'icon': '🐳'},
    {'id': 'cicd', 'name': 'CI/CD', 'icon': '🔁'},
    {'id': 'aws', 'name': 'AWS', 'icon': '☁️'},
    {'id': 'kubernetes', 'name': 'Kubernetes', 'icon': '⚙️'},
    {'id': 'terraform', 'name': 'Terraform', 'icon': '🛠️'},
    {'id': 'ansible', 'name': 'Ansible', 'icon': '📦'},
]


def load_data():
    """Read all saved submissions from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(data):
    """Write the full submissions list back to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'backend': 'Flask Backend',
        'status': 'Running',
        'message': 'DevOps backend is healthy'
    })


@app.route('/api/tools', methods=['GET'])
def tools():
    return jsonify(TOOLS)


@app.route('/api/submit', methods=['POST'])
def submit():
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get('name') or '').strip()
    tool = (body.get('tool') or '').strip()

    if not name or not tool:
        return jsonify({'error': 'name and tool are required'}), 400

    data = load_data()
    entry = {
        'id': (data[-1]['id'] + 1) if data else 1,
        'name': name,
        'tool': tool
    }
    data.append(entry)
    save_data(data)  # <-- persisted to data.json here

    return jsonify({
        'message': f'Submitted! {name} selected {tool}',
        'entry': entry
    })


@app.route('/api/submissions', methods=['GET'])
def submissions():
    """Return everything currently saved in data.json."""
    return jsonify(load_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)