from flask import Blueprint, jsonify, request

bpMain = Blueprint('bpMain', __name__)

@bpMain.route('/')
def main():
    return jsonify({
        "welcome": "myAPI test with Flask"
    }), 200