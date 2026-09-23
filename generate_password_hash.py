import base64, hashlib, getpass, secrets

ITERATIONS = 310_000
password = getpass.getpass("Owner password: ")
if len(password) < 12:
    raise SystemExit("Use uma password com pelo menos 12 caracteres.")
salt = secrets.token_bytes(16)
digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
print("pbkdf2_sha256$%d$%s$%s" % (ITERATIONS, base64.urlsafe_b64encode(salt).decode(), base64.urlsafe_b64encode(digest).decode()))
