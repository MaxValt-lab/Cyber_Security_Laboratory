# risk_engine.py

import hashlib
import json
from datetime import datetime

class RiskEngine:
    def __init__(self, policy_path="risk_policy.json"):
        self.policy = self.load_policy(policy_path)

    def load_policy(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("[!] Политика риска не найдена. Используется пустая.")
            return {}

    def assess_event(self, event):
        score = 0
        tags = []

        if "type" in event:
            score += self.policy.get("type_weights", {}).get(event["type"], 0)
            tags.append(event["type"])

        if "source" in event:
            score += self.policy.get("source_weights", {}).get(event["source"], 0)
            tags.append(event["source"])

        if "severity" in event:
            score += self.policy.get("severity_weights", {}).get(event["severity"], 0)
            tags.append(event["severity"])

        result = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "risk_score": score,
            "tags": tags,
            "hash": hashlib.sha256(json.dumps(event).encode()).hexdigest()
        }

        return result