from flask import Flask, request, jsonify, abort
from server import BackendServer
import sys
import os

app = Flask(__name__)
server = BackendServer(os.environ['SERVER_PRIVATE_KEY'])

@app.route('/register', methods=['GET', 'POST'])
def registration_handler():
    throw_if_invalid_request(request, ['username', 'user_salt', 'user_verifier'])
    content = request.get_json()
    if len(content['username']) > 79:
        return error(400, "Passed in info bad")
    if 'use_crypto' in content:
        if (server.register_user_encrypted(content['username'], content['user_salt'], content['user_verifier'])):
            return jsonify({'r':'registered'})
        else:
            return error(400, 0)
    else:
        if (server.register_user(content['username'], content['user_salt'], content['user_verifier'])):
            return jsonify({'r':'registered'})
        else:
            return error(400, 0)

@app.route('/login/get_salt', methods=['GET', 'POST'])
def login_get_salt_handler():
    throw_if_invalid_request(request, ['username'])
    content = request.get_json()
    salt = server.get_user_salt(content['username'])
    if len(salt) == 0:
        return error(400, 0)
    else:
        return jsonify({'user_salt': salt})

@app.route('/login/get_b', methods=['GET', 'POST'])
def login_get_b_handler():
    throw_if_invalid_request(request, ['username', 'big_a'])
    content = request.get_json()
    if 'use_crypto' in content:
        B, n = server.create_user_session_encrypted(content['username'], content['big_a'])
    else:
        B, n = server.create_user_session(content['username'], content['big_a'])
    if len(B) == 0:
        return error(400, 0)
    return jsonify({'big_b': B, 'nonce': n})

@app.route('/login/get_m2', methods=['GET', 'POST'])
def login_get_m2_handler():
    throw_if_invalid_request(request, ['username', 'm1', 'session_id', 'device_id'])
    content = request.get_json()
    if 'use_crypto' in content:
        m2 = server.validate_user_session_encrypted(content['username'], content['session_id'], content['m1'], content['device_id'])
    else:
        m2 = server.validate_user_session(content['username'], content['session_id'], content['m1'], content['device_id'])
    return jsonify({'m2': m2})

@app.route('/login/terminate', methods=['GET', 'POST'])
def login_terminate_handler():
    throw_if_invalid_request(request, ['username', 'session_id'])
    content = request.get_json()
    server.terminate_user_session(content['username'], content['session_id'])
    return jsonify({'s': 's'})

@app.route('/all_tickers')
def get_all_tickers():
    return jsonify(server.get_tickers())

@app.route('/user_tickers', methods=['GET', 'POST'])
def get_user_tickers():
    throw_if_invalid_request(request, ['username', 'session_id'])
    content = request.get_json()
    data = server.get_user_tickers(content['username'], content['session_id'])
    return jsonify(data)
    
@app.route('/add_ticker', methods=['GET', 'POST'])
def add_user_to_ticker():
    throw_if_invalid_request(request, ['username', 'session_id', 'tickers'])
    content = request.get_json()
    server.add_user_to_tickers(content['username'], content['session_id'], content['tickers'])
    return jsonify({'s': 's'})

@app.route('/delete_ticker', methods=['GET', 'POST'])
def remove_user_from_ticker():
    throw_if_invalid_request(request, ['username', 'session_id', 'tickers'])
    content = request.get_json()
    server.remove_user_from_tickers(content['username'], content['session_id'], content['tickers'])
    return jsonify({'s': 's'})

@app.errorhandler(Exception)
def exception_handler(e):
    return error(500, "Internal Error: "+str(e))

@app.errorhandler(ValueError)
def valueerror_handler(e):
    return error(400, "Bad argument: "+str(e))

@app.errorhandler(TypeError)
def typeerror_handler(e):
    return error(400, str(e))

def throw_if_invalid_request(request, expected_fields):
    if (request.is_json is not True):
        raise ValueError('Request not json format')
    content = request.get_json()
    for field in expected_fields:
        if not field in content:
            raise ValueError('Field '+str(field)+' expected but not found')

def error(code, failure_num):
    response = jsonify({
        'status': code,
        'error': failure_num
    })
    response.status_code = code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
