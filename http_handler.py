from flask import Flask, request, jsonify, abort
from server import BackendServer

app = Flask(__name__)
server = BackendServer()

@app.route('/')
def root():
    return 'Hello, World!'

@app.route('/register', methods=['GET', 'POST'])
def registration_handler():
    throw_if_invalid_request(request, ['username', 'user_salt', 'user_verifier'])
    content = request.get_json()
    if (len(content['user_salt']) != 256 or
        len(content['user_verifier']) != 256 or
        len(content['username']) > 79):
        return error(400, 1)
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
    B, n = server.create_user_session(content['username'], content['big_a'])
    if len(B) == 0:
        return error(400, 0)
    return jsonify({'big_b': B, 'nonce': n})

@app.route('/login/get_m2', methods=['GET', 'POST'])
def login_get_m2_handler():
    throw_if_invalid_request(request, ['username', 'm2', 'hnonce'])
    content = request.get_json()
    m2 = server.validate_user_session(content['username'], content['m2'], content['hnonce'])
    return jsonify({'m2': m2})

@app.errorhandler(Exception)
def exception_handler(e):
    return error(400, "Bad Arguments: "+str(e))

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
