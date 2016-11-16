import socket
from hashlib import sha256

def command(comm):
	s = socket.socket(socket.AF_UNIX)
	s.connect("/tmp/minecraft_worker/1")
	s.sendall(comm.encode())
	res = s.recv(256)
	s.close()
	return res.decode()

def write_page():
	data = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>
Worker control panel
</title>
<link rel="stylesheet" type="text/css" href="style" />
</head>
<body>
<table>
<tr>
<th colspan='2'> Bot manager</th>
</tr>
"""
	users = command("showworkers").split('\n')
	for i in users:
		if i:
			data += "<tr><td class='norm'>"+i+"</td><td class='add'><a href='stop?username="+i+"'>-</a></td></tr>"
	data += """
<tr><td class='norm'>
<input onblur='document.getElementById("rem").href=\"create?username=\"+this.value'>

</td><td class='rem'><a id='rem' href='create'>+</a></td></tr>

</table>
</html>
"""
	return data

def login_page(salt, fail=False):
	page = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<link rel="stylesheet" type="text/css" href="style" />
<title>
</title>
<script type="text/javascript" src="../res/sha256.min.js"></script>
<script type="text/javascript">
function enc(str) {
	return(sha256(sha256(str+"8cbbcf")+"%s"));
}
function update_link() {
	u = document.getElementById("login").value
	p = enc(document.getElementById("password").value)
	document.getElementById("go").href = "auth?username="+u+"&passwd="+p
}
</script>
</head>
<body>
<table>
<tr>
<th colspan=3>
Sign in
</th>
<tr>
<td class="norm">Login:</td><td class="norm" onblur="update_link()"><input id="login" /><td rowspan=2 style="background-color: #AFA"><a style="width:0.8cm" id="go" href="auth"> &gt; </a></td>
</tr>
<tr>
<td class="norm">Password:</td><td class="norm"><input type="password" %s id="password" onblur="update_link()"/></td>
</tr>
</table>
</body>
</html>
""" % (salt, "style='background-color: #fcc'" if fail else "")

	return page

