from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import requests
import json
from datetime import datetime

class CyberSecApp(App):
    def build(self):
        self.title = "Cyber Security Lab"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(text='Cyber Security Laboratory', size_hint_y=None, height=50, 
                      color=(1,1,1,1), font_size=20)
        main_layout.add_widget(header)
        
        # Server input
        server_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        server_layout.add_widget(Label(text='Server:', size_hint_x=0.3))
        self.server_input = TextInput(text='http://192.168.1.100:8000', multiline=False)
        server_layout.add_widget(self.server_input)
        main_layout.add_widget(server_layout)
        
        # Event inputs
        event_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        
        type_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        type_layout.add_widget(Label(text='Type:', size_hint_x=0.3))
        self.type_input = TextInput(text='mobile_event', multiline=False)
        type_layout.add_widget(self.type_input)
        event_layout.add_widget(type_layout)
        
        severity_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        severity_layout.add_widget(Label(text='Severity:', size_hint_x=0.3))
        self.severity_input = TextInput(text='medium', multiline=False)
        severity_layout.add_widget(self.severity_input)
        event_layout.add_widget(severity_layout)
        
        message_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        message_layout.add_widget(Label(text='Message:', size_hint_x=0.3))
        self.message_input = TextInput(text='Mobile security event', multiline=False)
        message_layout.add_widget(self.message_input)
        event_layout.add_widget(message_layout)
        
        main_layout.add_widget(event_layout)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        send_btn = Button(text='Send Event', background_color=(0.2, 0.6, 1, 1))
        send_btn.bind(on_press=self.send_event)
        button_layout.add_widget(send_btn)
        
        status_btn = Button(text='Check Status', background_color=(0.2, 0.8, 0.2, 1))
        status_btn.bind(on_press=self.check_status)
        button_layout.add_widget(status_btn)
        
        stats_btn = Button(text='Get Stats', background_color=(0.8, 0.6, 0.2, 1))
        stats_btn.bind(on_press=self.get_stats)
        button_layout.add_widget(stats_btn)
        
        main_layout.add_widget(button_layout)
        
        # Response area
        self.response_label = Label(text='Ready...', text_size=(None, None), 
                                   valign='top', halign='left')
        scroll = ScrollView()
        scroll.add_widget(self.response_label)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def send_event(self, instance):
        try:
            server = self.server_input.text.strip()
            event_data = {
                "type": self.type_input.text.strip(),
                "source": "mobile",
                "severity": self.severity_input.text.strip(),
                "message": self.message_input.text.strip()
            }
            
            response = requests.post(f"{server}/api/event", 
                                   json=event_data, timeout=10)
            result = response.json()
            
            self.response_label.text = f"Event sent successfully!\nRisk Score: {result.get('risk_score', 0)}\nAction: {result.get('action', 'none')}\nTime: {datetime.now().strftime('%H:%M:%S')}"
            
        except Exception as e:
            self.response_label.text = f"Error sending event: {str(e)}"
    
    def check_status(self, instance):
        try:
            server = self.server_input.text.strip()
            response = requests.get(f"{server}/api/status", timeout=10)
            result = response.json()
            
            self.response_label.text = f"Server Status: {result.get('status', 'unknown')}\nTime: {datetime.now().strftime('%H:%M:%S')}"
            
        except Exception as e:
            self.response_label.text = f"Error checking status: {str(e)}"
    
    def get_stats(self, instance):
        try:
            server = self.server_input.text.strip()
            response = requests.get(f"{server}/api/stats", timeout=10)
            result = response.json()
            
            self.response_label.text = f"Statistics:\nTotal Events: {result.get('total_events', 0)}\nTotal Incidents: {result.get('total_incidents', 0)}\nAverage Risk: {result.get('average_risk_score', 0)}\nTime: {datetime.now().strftime('%H:%M:%S')}"
            
        except Exception as e:
            self.response_label.text = f"Error getting stats: {str(e)}"

if __name__ == '__main__':
    CyberSecApp().run()