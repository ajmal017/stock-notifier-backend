import socket
import sys
import server_login
import scraper
import database
import first_time

class BackendServer:

    def __init__(self):
        self.login_lib = server_login.ServerLoginLibrary()
        self.user_login_info = {}
        self.user_sessions = {}

        
    def register_user(self, username, user_salt, user_verifier):
        if(username in self.user_login_info):
            return False
        self.user_login_info[username] = {'s': self.login_lib.hexToBytes(user_salt),
                                          'v': self.login_lib.hexToBytes(user_verifier)}
        return True

    def get_user_salt(self, username):
        if(not username in self.user_login_info):
            return ""
        return self.login_lib.bytesToHex(self.user_login_info[username]['s'])

    def create_user_session(self, username, a_hex):
        if(not username in self.user_login_info):
            return ("", "")
        v = self.user_login_info[username]['v']
        b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(v)
        if(not username in self.user_sessions):
            self.user_sessions[username] = {h_bytes : {'A': self.login_lib.hexToBytes(a_hex),
                                                       'b': b_bytes,
                                                       'B': B_bytes}}
        else:
            while (h_bytes in self.user_sessions[username]):
                b_bytes, B_bytes, n_bytes, h_bytes = self.login_lib.generate_b(v)
            self.user_sessions[username][h_bytes] = {'A': self.login_lib.hexToBytes(a_hex),
                                                     'b': b_bytes,
                                                     'B': B_bytes}
        return (self.login_lib.bytesToHex(B_bytes),
                self.login_lib.bytesToHex(n_bytes))

    def validate_user_session(self, username, h_hex, mv_hex):
        if(not username in self.user_sessions):
            return bytearray()
        h = self.login_lib.hexToBytes(h_hex)
        if (not h in self.user_sessions[username]):
            return bytearray()
        session_data = self.user_sessions[username][h]
        login_data = self.user_login_info[username]
        sk, m1, m2 = self.login_lib.generate_sk(username,
                                                session_data['A'],
                                                session_data['b'],
                                                session_data['B'],
                                                login_data['s'],
                                                login_data['v'])
        mv = self.login_lib.hexToBytes(mv_hex)
        if (mv_hex != m1):
            return bytearray()
        self.user_sessions[username][h]['k'] = sk
        return self.login_lib.bytesToHex(m2)

    def is_user_logged_in(self, username):
        if(not username in self.user_sessions):
            return False
        session_data = self.user_sessions[username]
        for session in session_data:
            if 'k' in session:
                return True
        return False

    def get_tickers(self):
        return database.getTickers()
    

def run_server():
    print("Starting test")

    symbols = first_time.tickers
    
    stock_data = scraper.getStockData(symbols)
    print(stock_data)
"""
    for symbol, data in stock_data.items():
        database.updateSupports(symbol, [i[0] for i in data['Supports']])
        database.updateResistances(symbol, [i[0] for i in data['Resistances']])
        
    user_tickers = database.getTickersFromUser('Aldaddy')
    print(user_tickers)

    try:
        server_lib = server_login.ServerLoginLibrary()
    except Exception:
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 8000)
    sock.bind(server_address)
    sock.listen(1)
    connection, client_address = sock.accept()
    s_bytes = connection.recv(128)
    v_bytes = connection.recv(128)
    A_bytes = connection.recv(128)
    b_bytes, B_bytes = server_lib.generate_b(v_bytes)
    connection.send(B_bytes)
    m1_bytes, m2_bytes = server_lib.generate_ss(A_bytes, b_bytes, B_bytes, v_bytes)
    mv = connection.recv(64)
    connection.send(m2_bytes)
    if mv == m1_bytes:
        print("Login success :)")
    else:
        print("Login failure :(")
"""


if __name__ == "__main__":
    run_server()
