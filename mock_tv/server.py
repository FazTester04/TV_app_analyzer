from flask import Flask, jsonify, request
import time

app = Flask(__name__)

state = {
    "power": False,
    "volume": 10,
    "app": None,
    "playing": False
}

@app.route('/ping')
def ping():
    return jsonify({"ok": True, "time": time.time()})

@app.route('/power', methods=['POST'])
def power():
    data = request.get_json() or {}
    state['power'] = bool(data.get('on', not state['power']))
    return jsonify({"power": state['power']})

@app.route('/app/launch', methods=['POST'])
def launch_app():
    data = request.get_json() or {}
    app_name = data.get('app')
    if not app_name:
        return jsonify({"error": "no app specified"}), 400
    # simulate a small delay
    time.sleep(0.5)
    state['app'] = app_name
    state['playing'] = False
    return jsonify({"launched": app_name})

@app.route('/app/play', methods=['POST'])
def play():
    data = request.get_json() or {}
    title = data.get('title')
    if not state['app']:
        return jsonify({"error": "no app launched"}), 400
    # simulate failure for specific title (demo of crash)
    if title and 'crash' in title.lower():
        return jsonify({"error": "playback crashed", "code": "TimeoutError"}), 500
    state['playing'] = True
    return jsonify({"playing": True, "title": title})

@app.route('/status')
def status():
    return jsonify(state)

if __name__ == '__main__':
    app.run(debug=True)
