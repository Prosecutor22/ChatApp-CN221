import hashlib
password = 'minhpp'
salt = "KTML"
key = password+salt
hashed = hashlib.md5(key.encode('utf-8'))
print(hashed.hexdigest())