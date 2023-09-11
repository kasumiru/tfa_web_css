#!/usr/bin/python3

import json
import time
from flask import Flask, jsonify, request, render_template
import pyotp

app = Flask(__name__)

class clr:
    green     = '\033[92m'
    yellow    = '\033[93m'
    red       = '\033[91m'
    blue      = '\033[94m'
    cyan      = '\033[96m'
    magenta   = '\033[95m'
    grey      = '\033[90m'
    rest      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
#print(f"{clr.green} Hellllloooow  {clr.rest}")
#print(clr.red + "Hellloowwww" + clr.rest)



@app.errorhandler(404)
def page_not_found(error):
    return "Aborted with 404 key is not valid", 404

@app.route("/ping", methods=['GET'])
def ping():
    return 'pong'


with open(f'keys.json', 'r') as f:
   keys = json.load(f)


def get_seconds() -> int:
    max = 60
    seconds = int(time.strftime("%S"))
    if seconds >= 30:
        sec = max - seconds
    else:
        sec = max - seconds - 30
    return sec


def get_totp_by_route(route) -> dict:
    route = route.replace("/","").replace('-back','').replace('-dev','')
    totp = keys.get(route).replace(" ", "").strip()
    totp_code = pyotp.TOTP(totp).now()

    return jsonify(
        {
            "totp_code": totp_code,
            "path": request.path,
            "seconds": get_seconds()

        }
    ) # type: ignore


@app.route("/")
def first_line_cc03():
    route = request.path.replace("/","")
    # return render_template('backend.html', arg_url=f'{route}-back')
    return render_template('backend.html', arg_url=f'back')
@app.route("/back")
def first_line_cc03_back():
    # route = request.path
    route = 'main'
    resp_dict = get_totp_by_route(route)
    return resp_dict



if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=80
        )
