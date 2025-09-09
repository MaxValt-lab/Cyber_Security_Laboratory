"""
GitHub repository configuration script
"""
import requests
import os
import json

# Константы
REPO_OWNER = "MaxValt-lab"
REPO_NAME = "Cyber_Security_Laboratory"
GITHUB_API = "https://api.github.com"

# Функции настройки
def setup_branch_protection(token):
    """Настройка защиты ветки master"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    protection_rules = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["security-checks", "docker-build"]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismissal_restrictions": {},
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1
        },
        "restrictions": None
    }
    
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/branches/master/protection"
    response = requests.put(url, headers=headers, json=protection_rules)
    return response.status_code == 200

def enable_security_features(token):
    """Включение функций безопасности"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    # Включаем Dependabot
    dependabot_config = {
        "updates": [
            {
                "package-ecosystem": "pip",
                "directory": "/",
                "schedule": {"interval": "daily"}
            },
            {
                "package-ecosystem": "docker",
                "directory": "/",
                "schedule": {"interval": "weekly"}
            }
        ]
    }
    
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/vulnerability-alerts"
    response = requests.put(url, headers=headers)
    
    # Сохраняем конфигурацию Dependabot
    with open('.github/dependabot.yml', 'w') as f:
        json.dump(dependabot_config, f, indent=2)
    
    return True

def main():
    """Основная функция настройки"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        return False
    
    print("Setting up branch protection...")
    if setup_branch_protection(token):
        print("Branch protection configured successfully")
    else:
        print("Failed to configure branch protection")
        
    print("Enabling security features...")
    if enable_security_features(token):
        print("Security features enabled successfully")
    else:
        print("Failed to enable security features")

if __name__ == "__main__":
    main()