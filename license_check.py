import hashlib
import sys

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        print(f"[ERROR] Файл {path} не найден.")
        sys.exit(1)

def load_signature(path="code-signature.txt"):
    signatures = {}
    try:
        with open(path, "r") as f:
            for line in f:
                if ":" in line and not line.startswith("#"):
                    file, hash_val = line.strip().split(":")
                    signatures[file.strip()] = hash_val.strip()
    except FileNotFoundError:
        print("[ERROR] Файл code-signature.txt не найден.")
        sys.exit(1)
    return signatures

def verify_files():
    signatures = load_signature()
    for file, expected_hash in signatures.items():
        actual_hash = hash_file(file)
        if actual_hash != expected_hash:
            print(f"[FAIL] Нарушение целостности: {file}")
            print(f"Ожидалось: {expected_hash}")
            print(f"Получено:  {actual_hash}")
            sys.exit(1)
        else:
            print(f"[OK] {file} — проверка пройдена.")

if __name__ == "__main__":
    print("[🔐] Проверка лицензии и цифровых подписей...")
    verify_files()
    print("[✅] Все файлы прошли проверку.")