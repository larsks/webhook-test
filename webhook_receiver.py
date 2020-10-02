import flask
import hmac
import json
import logging
import os

app = flask.Flask(__name__)
seq = 0


logging.basicConfig(level=logging.INFO)

HMAC_SECRET = os.environ.get('HOOK_HMAC_SECRET').encode()


@app.route('/hook', methods=['POST'])
def webhook_receive():
    global seq

    sig = flask.request.headers.get('x-hub-signature')
    if sig is None:
        app.logger.warning('no signature')
    else:
        alg, sig = sig.split('=', 1)
        hasher = hmac.HMAC(HMAC_SECRET, digestmod=alg)
        hasher.update(flask.request.data)
        if hasher.hexdigest() != sig:
            app.logger.warning('failed signature')

    with open(f'req-{seq}.json', 'w') as fd:
        cwd = os.getcwd()
        json.dump({
            'headers': dict(flask.request.headers),
            'body': flask.request.json
        }, fd, indent=2)
        app.logger.info(f'wrote request {seq} ({cwd})')
        seq += 1

    return "Thanks."


if __name__ == '__main__':
    app.run(port=8383)
