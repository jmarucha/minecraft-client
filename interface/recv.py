import socket

s = socket.socket(socket.AF_UNIX)

s.bind("/tmp/tmpsock")
s.listen(1)
while 1:
	conn,addr = s.accept()
	with conn:
		print(conn.recv(1024))

