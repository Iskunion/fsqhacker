import base64
import hashlib

def hashfile(name):
    f = open(name, "rb")
    hasher = hashlib.sha256(f.read())
    base64sha = base64.b64encode(hasher.digest())
    f.close()
    return base64sha