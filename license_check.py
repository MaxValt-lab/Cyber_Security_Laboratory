import hashlib

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def verify(path, expected_hash):
    actual = hash_file(path)
    if actual != expected_hash:
        raise Exception(f"Файл {path} повреждён или изменён.")

verify("LICENSE.md", "3f2c8d1e9a7b4c6d8e2f1a3b9c0d7e6f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6")