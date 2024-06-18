from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def do():
    return jsonify({"status": "active", "name": "PW link changer"})