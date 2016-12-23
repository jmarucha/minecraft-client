#!/usr/bin/python3


import socket
import m_utility

class Connection:
	def __init__(self, host ='localhost', port=25565, username='c666'):
		self._host = host
		self._port = port
		self._connected = 0
		self._compression = 0
		self._username = username 
	def connect(self):
		if self._connected == 1:
			self._connection.close()
		self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._connection.settimeout(5.0)
		self._connection.connect((self._host,self._port))
		self._connection.settimeout(5.0)
		self._comperssion = 0
	def login(self):
		self._send_package(("byte",0),("varint",210),("string","localhost"),("short",25565),("byte",2)) #initial handshake
		self._send_package(("byte",0),("string",self._username)) #login
		
	def _write_string(self,string):
		return m_utility.varInt(len(string.encode()))+string.encode()
	def _send_package(self, *args):
		data = b''
		for arg in args:
			if arg[0]=='byte':
				data += bytes([arg[1]])
			if arg[0]=='int':
				data += arg[1].to_bytes(4,byteorder='little')
			if arg[0]=='short':
				data += arg[1].to_bytes(2,byteorder='little')
			if arg[0]=='string':
				data += self._write_string(arg[1])
			if arg[0]=='long':
				data += arg[1].to_bytes(8,byteorder='little')
			if arg[0]=='varint':
				data += m_utility.varInt(arg[1]) 
			if arg[0]=='bin':
				data += arg[1]
		if self._compression == 0:
			self._connection.send(m_utility.varInt(len(data))+data)
		else:
			data = b'\x00'+data
			self._connection.send(m_utility.varInt(len(data))+data)
	def _get_varInt(self):
		res = 0
		i = 0
		while(True):
			temp = ord(m_utility.get_bytes(1,self._connection))
			res |= (temp & 0x7F) << 7*(i)
			i = i+1
			if not temp & 0x80:
				break
		return (res,i)
	def _read_varInt(self,data,i0):
		res = 0
		i = i0
		while(True):
			temp = data[i]
			res |= (temp & 0x7F) << 7*(i-i0)
			i = i+1
			if not temp & 0x80:
				break
		return (res,i)
	def _read_str(self,data, i0):
		(l,i1) = self._read_varInt(data,i0)
		return (data[i1:i1+l].decode(),i1+l)
	def get_package(self):
		if (self._compression == 0):
			l = self._get_varInt()[0]
			pack_id = ord(m_utility.get_bytes(1,self._connection))
			data = m_utility.get_bytes(l-1,self._connection)
			if (pack_id == 0x03):
				self._compression = 1
				self._compth = self._read_varInt(data,0)[0]
		else:
			l = self._get_varInt()[0]
			data = m_utility.get_bytes(l,self._connection)
			(data_l,i_start) = self._read_varInt(data,0)
			if data_l < self._compth:
				pack_id = data[i_start]
			else:
				pack_id = 0x99
		return (pack_id, data)
def main():
	client = Connection()
	client.connect()
	client.login()
	
	
	
	while (1):
		(pid,data)=client.get_package()
		if (pid != 0):
			print(('%02x : '%pid)+data[0:32].hex())
		if (pid==0x1F): #keepalive packet id
			print("KEEPALIVE")
			keepAliveID=data[2:]
			print(keepAliveID)
			client._send_package(("byte",0x0B),("bin",keepAliveID))

if __name__ == "__main__":
	main()
