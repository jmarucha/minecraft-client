from hashlib import sha256
salt = "my_salt"
dict = {'username': sha256('password'+salt)
}
