import server_login
import crypto
import database
import sys
import base64

class BackendServer:

    def __init__(self, private_key):
        self.login_lib = server_login.ServerLoginLibrary()
        self.crypto_lib = crypto.CryptoLib(private_key)

    def register_user_encrypted(self, username, user_salt, user_verifier):
        if(database.userExists(username)):
            raise TypeError("Username Taken")
        database.newUser(username, [base64.b64encode(self.crypto_lib.rsa_decrypt(user_salt)),
                                    base64.b64encode(self.crypto_lib.rsa_decrypt(user_verifier)),
                                    b''], [])
        return True
        
    def register_user(self, username, user_salt, user_verifier):
        if(database.userExists(username)):
            raise TypeError("Username Taken")
        database.newUser(username, [base64.b64encode(self.login_lib.hexToBytes(user_salt)),
                                    base64.b64encode(self.login_lib.hexToBytes(user_verifier)),
                                    b''], [])
        return True

    def get_user_salt_b64(self, username):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        login_data = database.getLoginDataFromUser(username)
        return login_data[0]


    def get_user_salt(self, username):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        login_data = database.getLoginDataFromUser(username)
        return self.login_lib.bytesToHex(base64.b64decode(login_data[0]))

    def create_user_session_encrypted(self, username, a_b64):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        login_data = database.getLoginDataFromUser(username)
        b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(base64.b64decode(login_data[1]))
        currentSessions = database.getSessionsFromUser(username)
        if (currentSessions is not None):
            while (h_bytes in currentSessions):
                b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(v)
        database.newSession(username,
                            base64.b64encode(h_bytes),
                            base64.b64encode(self.crypto_lib.rsa_decrypt(a_b64)),
                            base64.b64encode(b_bytes),
                            base64.b64encode(B_bytes),
                            b'',
                            b'')
        return (base64.b64encode(B_bytes),
                base64.b64encode(n_bytes))


    def create_user_session(self, username, a_hex):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        login_data = database.getLoginDataFromUser(username)
        b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(base64.b64decode(login_data[1]))
        currentSessions = database.getSessionsFromUser(username)
        if (currentSessions is not None):
            while (h_bytes in currentSessions):
                b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(v)
        database.newSession(username,
                            base64.b64encode(h_bytes),
                            base64.b64encode(self.login_lib.hexToBytes(a_hex)),
                            base64.b64encode(b_bytes),
                            base64.b64encode(B_bytes),
                            b'',
                            '')
        return (self.login_lib.bytesToHex(B_bytes),
                self.login_lib.bytesToHex(n_bytes))

    def validate_user_session_encrypted(self, username, h_b64, mv_b64, deviceID):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        session = database.getSessionInts(username, h_b64)
        if (session is None):
            return "Session error"
        login_data = database.getLoginDataFromUser(username)
        sk, m1, m2 = self.login_lib.generate_sk(username,
                                                base64.b64decode(session['a']),
                                                base64.b64decode(session['b']),
                                                base64.b64decode(session['b2']),
                                                base64.b64decode(login_data[0]),
                                                base64.b64decode(login_data[1]))
        mv = self.crypto_lib.rsa_decrypt(mv_hex)        
        if (mv != m1):
            raise TypeError("Invalid Password")
        database.editSessionKey(username, base64.b64encode(h), base64.b64encode(sk), deviceID)
        return base64.b64encode(m2)

                            
    def validate_user_session(self, username, h_hex, mv_hex, deviceID):
        if(not database.userExists(username)):
            raise TypeError("Username does not exist")
        h = self.login_lib.hexToBytes(h_hex)
        session = database.getSessionInts(username, base64.b64encode(h))
        if (session is None):
            return "Session error"
        login_data = database.getLoginDataFromUser(username)
        sk, m1, m2 = self.login_lib.generate_sk(username,
                                                base64.b64decode(session['a']),
                                                base64.b64decode(session['b']),
                                                base64.b64decode(session['b2']),
                                                base64.b64decode(login_data[0]),
                                                base64.b64decode(login_data[1]))
        mv = self.login_lib.hexToBytes(mv_hex)        
        if (mv != m1):
            raise TypeError("Invalid Password")
        database.editSessionKey(username, base64.b64encode(h), base64.b64encode(sk), deviceID)
        return self.login_lib.bytesToHex(m2)
                            
    def terminate_user_session(self, username, session):
        session_id = base64.b64encode(self.login_lib.hexToBytes(session))
        database.deleteSession(username, session_id)
            
    def get_tickers(self):
        return database.getTickers()

    def get_user_tickers(self, username, session):
        session_id = base64.b64encode(self.login_lib.hexToBytes(session))
        key = database.getSessionK(username, session_id)
        if key is None:
            raise ValueError('User session not valid')
        tickers = database.getTickersFromUser(username)
        ticker_data = []
        for t in tickers:
            data = database.getRecordForTicker(t)
            data.pop('_id', None)
            data.pop('users', None)
            supports = []
            for price, strength in data['supports']:
                supports.append({'price': price, 'strength': strength})
            data['supports'] = supports
            resistances = []
            for price, strength in data['resistances']:
                resistances.append({'price': price, 'strength': strength})
            data['resistances'] = resistances
            ticker_data.append(data)
            
        return ticker_data

    def add_user_to_tickers(self, username, session, tickers):
        session_id = base64.b64encode(self.login_lib.hexToBytes(session))
        key = database.getSessionK(username, session_id)
        if key is None:
            raise ValueError('User session not valid')
        database.addTickersToUser(username, tickers)

    def remove_user_from_tickers(self, username, session, tickers):
        session_id = base64.b64encode(self.login_lib.hexToBytes(session))
        key = database.getSessionK(username, session_id)
        if key is None:
            raise ValueError('User session not valid')
        database.removeTickersFromUser(username, tickers)
