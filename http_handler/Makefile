default: server

server:	
	@g++ -shared -L/root/.local/lib -I/root/.local/include -lgmp -lsodium -o server_lib.so -fPIC server_login.cpp