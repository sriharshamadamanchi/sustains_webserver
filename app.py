from flask import request, jsonify

from src.factory import create_app

app = create_app()


@app.route("/")
def sustains_server():
    return "<p>Welcome to sustains server!</p>"


@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method == 'OPTIONS' or request.method == 'options': return jsonify(headers), 200


if __name__ == "__main__":
    app.run()
