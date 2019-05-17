import socket
import sys
import server_login
import scraper
import database

def run_server():
    print("Starting test")

    symbols = ["AMD", "MSFT", "SQ"]
    
    stock_data = scraper.getStockData(symbols)
    print(stock_data)

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
    while True:
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

if __name__ == "__main__":
    run_server()
