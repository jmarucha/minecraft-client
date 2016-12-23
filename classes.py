#!/usr/bin/python3

import threading
from time import sleep
from connection import Connection
import struct

class Idler (threading.Thread):
	def __init__(self, username="c666", host="127.0.0.1", port = 25565):
		threading.Thread.__init__(self)
		self.connection=Connection(host=host,port=port,username=username)
		self.stop=False
	def run(self):
		self.connection.connect()
		self.connection.login()
		while (1):
			(pid,data)=self.connection.get_package()
			if (pid==0x1F): #keepalive packet id
				keepAliveID=data[2:]
				self.connection._send_package(("byte",0x0B),("bin",keepAliveID))
			if (self.stop):
				break


class Attacker (threading.Thread):
	def __init__(self, username="c666", host="127.0.0.1", port = 25565, interval = 0.1, ):
		print(username)
		threading.Thread.__init__(self)
		self.connection=Connection(host=host,port=port,username=username)
	def run(self):
		self.connection.connect()
		self.connection.login()
		while (1):
			(pid,data)=self.connection.get_package()
			if (pid==0x1F): #keepalive packet id
				keepAliveID=data[2:]
				self.connection._send_package(("byte",0x0B),("bin",keepAliveID))
			if (pid==0x2E): #player position
				position = data[2:34]
				print(struct.unpack(">dddff",position))
				t_id=data[35:]
				self.connection._send_package(("byte",0x00),("bin",t_id))

def main():
	worker1 = Attacker(username="c666")
	worker1.start()
	while 1:
		sleep(1.0)
if __name__ == "__main__":
	main()
