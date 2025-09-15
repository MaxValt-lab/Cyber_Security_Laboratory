# notification_agent.py

from agent_logic import AgentLogic
import requests

class NotificationAgent(AgentLogic):
    def __init__(self):
        super().__init__("Notification")
        self.notification_channels = {
            "email": [],
            "telegram": [],
            "slack": []
        }
        self.api_keys = {
            "telegram": "YOUR_TELEGRAM_TOKEN",
            "slack": "YOUR_SLACK_TOKEN"
        }

    def add_recipient(self, channel: str, recipient: str):
        if channel in self.notification_channels:
            self.notification_channels[channel].append(recipient)

    def send_notification(self, message: str, channel: str = "email"):
        if channel == "email":
            self.send_email(message)
        elif channel == "telegram":
            self.send_telegram(message)
        elif channel == "slack":
            self.send_slack(message)

    def send_email(self, message: str):
        # Реализация отправки email
        self.logger.info(f"Отправка email: {message}")

    def send_telegram(self, message: str):
        url = f"https://api.telegram.org/bot{self.api_keys['telegram']}/sendMessage"
        for chat_id in self.notification_channels["telegram"]:
            params = {
                "chat_id": chat_id,
                "text": message
            }
            requests.post(url, params=params)
        self.logger.info(f"Сообщение отправлено в Telegram")

    def send_slack(self, message: str):
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.api_keys['slack']}"
        }
        for channel in self.notification_channels["slack"]:
            data = {
                "channel": channel,
                "text": message
            }
            requests.post(url, headers=headers, json=data)
        self.logger.info(f"Сообщение отправлено в Slack")