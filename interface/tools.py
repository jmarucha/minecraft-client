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
			data += "<tr><td class='norm'>"+i+"</td><td class='rem'><a href='stop?username="+i+"'>-</a></td></tr>"
	data += """
<tr><td class='norm'>
<input 
	onkeypress='if (event.keyCode == 13) {location.href="create?username="+this.value;return false;}'
	onblur='document.getElementById("rem").href=\"create?username=\"+this.value'>

</td><td class='add'><a id='rem' href='create'>+</a></td></tr>

</table>
</html>
"""
	return data

def login_page(salt, fail=False, perm_salt="",username=""):
	page = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<link rel="stylesheet" type="text/css" href="style" />
<title>
Worker control panel
</title>
<script type="text/javascript" src="../res/sha256.min.js"></script>
<script type="text/javascript">
function enc(str) {
	return(sha256(sha256(str+"%s")+"%s"));
}
function update_link() {
	u = document.getElementById("login").value
	p = enc(document.getElementById("password").value)
	document.getElementById("go").href = "auth?username="+u+"&passwd="+p
}

function next_field(e) {
	if (e.keyCode == 13) {
		document.getElementById("password").focus()
		return false;
	}
}

function key_submit(e) {
	if (e.keyCode == 13) {
		update_link()
		location.href=document.getElementById("go").href
		return false;
	}
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
<td class="norm">Login:</td><td class="norm" onblur="update_link()"><input value="%s" autofocus onkeypress="return next_field(event)" onblur="update_link()" id="login" /><td rowspan=2 style="background-color: #AFA"><a style="width:0.8cm" id="go" href="auth"> &gt; </a></td>
</tr>
<tr>
<td class="norm">Password:</td><td class="norm"><input type="password" %s id="password" onkeypress="return key_submit(event)" onblur="update_link()"/></td>
</tr>
</table>
</body>
</html>
""" % (perm_salt,salt, username, "style='background-color: #fcc'" if fail else "")

	return page

