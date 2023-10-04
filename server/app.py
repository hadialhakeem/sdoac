from flask import Flask, request, jsonify
from flask_cors import CORS
from extensions import neo4j

app = Flask(__name__)
CORS(app)

neo4j.connect()


@app.route("/")
def hello():
    return "Hello World"


@app.route("/path", methods=['POST'])
def generate():
    data = request.get_json(force=True)
    title = data['title']

    response_dict = {'title': title}
    return jsonify(response_dict)


@app.route("/search", methods=['POST'])
def search():
    data = request.get_json(force=True)
    title = data['title']

    response_dict = {'title': title}
    return jsonify(response_dict)


if __name__ == "__main__":
    app.run(debug=True)
