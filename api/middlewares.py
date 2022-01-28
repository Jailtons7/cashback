from flask import request, jsonify

from api import app


@app.before_request
def verify_headers_middleware():
    """
    Middleware to return BAD REQUEST if user
    call a POST without specify content-type as application/json
    """
    required = [
        request.method == 'POST',
        request.headers.get('Content-Type') != 'application/json'
    ]
    if all(required):
        return jsonify({'msg': 'Content-Type wrong or not set.'}), 400
