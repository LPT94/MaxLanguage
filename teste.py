import hashlib


senha = ""
print(hashlib.sha256(senha.encode("utf-8")).hexdigest())