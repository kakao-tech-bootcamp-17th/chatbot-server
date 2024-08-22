from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = {
        "code": e.code,
        "title": e.title,
        "description": e.description,
    }
    
    return jsonify(response)