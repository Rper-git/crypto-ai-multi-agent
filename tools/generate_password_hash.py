import getpass, secrets, hashlib
p=getpass.getpass("New password: ")
salt=secrets.token_bytes(16); iters=310000
d=hashlib.pbkdf2_hmac("sha256",p.encode(),salt,iters)
print(f"pbkdf2_sha256${iters}${salt.hex()}${d.hex()}")
