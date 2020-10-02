import flask
import json
import logging
import os

app = flask.Flask(__name__)
seq = 0


logging.basicConfig(level=logging.INFO)


@app.route('/hook', methods=['POST'])
def webhook_receive():
    print('cwd:', os.getcwd())
    global seq

    with open(f'req-{seq}.json', 'w') as fd:
        cwd = os.getcwd()
        json.dump(flask.request.json, fd, indent=2)
        app.logger.info(f'wrote request {seq} ({cwd})')
        seq += 1

    return "Thanks."


if __name__ == '__main__':
    app.run(port=8383)
