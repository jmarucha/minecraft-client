from mod_python import apache, util, Session
import socket
import tools
import cred
from hashlib import sha256
from random import randint
def index(req):
	sess = Session.Session(req)
	try:
		if(sess['logged']!=1):
			util.redirect(req, 'auth')
			return
	except KeyError:
		util.redirect(req, 'auth')
		return
	req.content_type = 'text/html'
	return tools.write_page()


def stop(req,username=""):
	sess = Session.Session(req)
	try:
		if(sess['logged']!=1):
			util.redirect(req, 'auth')
			return
	except KeyError:
		util.redirect(req, 'auth')
		return
	req.content_type = 'text/html'
	if (username!=""):
		tools.command("stop "+username)
	util.redirect(req, '.')

def create(req,username=""):
	sess = Session.Session(req)
	try:
		if(sess['logged']!=1):
			util.redirect(req, 'auth')
			return
	except KeyError:
		util.redirect(req, 'auth')
		return
	req.content_type = 'text/html'
	if (username!=""):
		tools.command("create "+username)
	util.redirect(req, '.')

def auth(req, username="", passwd=""):
	sess = Session.Session(req)
	sess.load()
	attempt = False
##	req.write(cred.dict['jan']+'\n')
##	req.write(sha256(cred.dict['jan']+sess['salt']).hexdigest())
	if not 'salt' in sess:
		sess['salt'] = ("%0.4X" % randint(0,256*256-1))+("%0.4X" % randint(0,256*256-1))
		sess.save()
	elif not username in cred.dict:
		sess['salt'] = ("%0.4X" % randint(0,256*256-1))+("%0.4X" % randint(0,256*256-1))
		sess.save()
	elif passwd==sha256((cred.dict[username]+sess['salt'])).hexdigest():
		sess['logged']=1
		sess.save()
		util.redirect(req,'.')
		return 
	else:
		sess['salt'] = ("%0.4X" % randint(0,256*256-1))+("%0.4X" % randint(0,256*256-1))
		sess.save()
	if passwd:
		attempt = True
	return tools.login_page(sess['salt'], fail=attempt,perm_salt=cred.salt,username=username)

def logout(req):
	sess = Session.Session(req)
	sess['logged']=0
	sess.save()
	util.redirect(req,'.')
	return

def style(req):
	req.content_type = 'text/css'
	return """
body {
	background-color: #666;
	font-family: Arial, sans-serif;
}
table {
	border: 1px solid;
	border-collapse: collapse;
	background-color: #fff;
	width: 6cm;
	position: absolute; top: 50%; left:50%; transform: translate(-50%, -50%)
}
th {
	height: 0.8cm;
	font-weight: bold;
	background-color: #CCC;
	line-height: 0.8cm;
}
td {
	border: 1px solid;
}
a {
	display: block;
	text-align: center;
	font-family: Arial,sans-serif;
	text-decoration: none;
	font-weight: bold;
	color: black;
	height: 100%;
	width: 100%;
	line-height: 0.8cm;
}
td.norm {
	padding-left: 0.15cm;
	height: 0.8cm;
	padding-right: 0.15cm;
}
td.add {
	background-color: #AFA;
	height: 0.8cm;
	width: 0.8cm;
}
td.rem {
	background-color: #FAA;
	height: 0.8cm;
	width: 0.8cm;
}
"""
