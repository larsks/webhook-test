import flask
import json

app = flask.Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_receive():
    print(json.dumps(flask.request.json, indent=2))
    return "Thanks."


if __name__ == '__main__':
    app.run(port=8383)
