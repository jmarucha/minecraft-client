#!/usr/bin/python3
# vim: tabstop=2:
import classes

import threading
import socket
import os,sys,stat
from time import sleep

class ControlPanel (threading.Thread):

	def __init__(self):
		self.workers=[]
		self.worker_names=[]
		threading.Thread.__init__(self)
	def run(self):
		with   socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
			os.mkdir("/tmp/minecraft_worker")
			s.bind("/tmp/minecraft_worker/1")
			s.listen(1)
			os.chmod("/tmp/minecraft_worker/1", stat.S_IRWXO)
			End = True
			while End:
				conn, addr = s.accept()
				with conn:
					while End:
						data = conn.recv(1024)
						if not data: break
						print(data)
						cmds = data.decode().split("\n")
						for i in cmds:
							cmd = i.split(" ")
							if (cmd[0]=="create"):
								if cmd[1] in self.worker_names:
									conn.sendall("chujaj sie\n".encode())
								else:
									self.workers.append(classes.Idler(username=cmd[1]))
									self.workers[-1].start()
									self.worker_names.append(cmd[1])
									conn.sendall(("created "+cmd[1]+"\n").encode())
							elif (cmd[0]=="stop"):
								try:
									x = self.worker_names.index(cmd[1])
									self.workers[x].stop=True
									self.workers[x].join()
									del self.workers[x]
									del self.worker_names[x]
									conn.sendall(("stopped "+cmd[1]+"\n").encode())
								except ValueError:
									conn.sendall("chujaj sie\n".encode())
							elif (cmd[0]=="showworkers"):
								tosend = ""
								if self.worker_names:
									print(self.worker_names)
									for i in self.worker_names:
										print(i)
										tosend+=(i+'\n')
									conn.sendall(tosend.encode())
								else:
									conn.sendall('\n'.encode())
								
							elif (cmd[0]=="echo"):
								conn.sendall("echo\n".encode())
							elif (cmd[0]=="exit"):
								for i in self.workers:
									i.stop=True
									i.join()
								End=False
							else:
								conn.sendall("\n".encode())
			os.remove("/tmp/minecraft_worker/1")
def main():
	c = ControlPanel()
	c.start()
	c.join()
if __name__=="__main__":
	main()	
