# audit_writer.py

from datetime import datetime

def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("audit.log", "a") as f:
        f.write(f"{timestamp} {message}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        log_event(" ".join(sys.argv[1:]))
    else:
        log_event("Событие без описания")