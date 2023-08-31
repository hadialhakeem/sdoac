from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/path", methods=['POST'])
def generate():
    data = request.get_json(force=True)
    title = data['title']

    response_dict = {'title': title}
    return jsonify(response_dict)


if __name__ == "__main__":
    app.run(debug=True)
