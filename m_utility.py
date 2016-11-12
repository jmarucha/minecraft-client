
def varInt(x):
	result = b''
	while True:
		temp = x & 0x7F # 0111111
		x = x>>7
		if x == 0:
			result += bytes([temp])
			return result
		else:
			result += bytes([temp|0x80])

def get_bytes(n, con):
#	data = b''
#	tmp = b''
#	while True:
	tmp=con.recv(n)
#		n = n -len(tmp)
#		data+=tmp
#		if n ==0:
#			break
	return tmp

