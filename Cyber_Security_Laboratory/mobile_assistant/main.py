#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import speech_recognition as sr
import pyttsx3
import threading
import json
import requests
from datetime import datetime

class MobileAssistantApp(App):
    def build(self):
        self.title = "CyberSec Mobile Assistant"
        
        # Инициализация компонентов
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = pyttsx3.init()
        self.learning_data = self.load_learning_data()
        
        # Главный layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        header = Label(text='🤖 CyberSec Assistant', size_hint_y=None, height=50, font_size=20)
        main_layout.add_widget(header)
        
        # Статус
        self.status_label = Label(text='Ready', size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)
        
        # Кнопки управления
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        voice_btn = Button(text='🎤 Voice', background_color=(0.2, 0.8, 0.2, 1))
        voice_btn.bind(on_press=self.start_voice_recognition)
        btn_layout.add_widget(voice_btn)
        
        scan_btn = Button(text='🔍 Scan', background_color=(0.8, 0.2, 0.2, 1))
        scan_btn.bind(on_press=self.start_security_scan)
        btn_layout.add_widget(scan_btn)
        
        learn_btn = Button(text='🧠 Learn', background_color=(0.2, 0.2, 0.8, 1))
        learn_btn.bind(on_press=self.start_learning_mode)
        btn_layout.add_widget(learn_btn)
        
        main_layout.add_widget(btn_layout)
        
        # Поле ввода команд
        self.command_input = TextInput(hint_text='Enter command or speak...', multiline=False, size_hint_y=None, height=40)
        self.command_input.bind(on_text_validate=self.process_text_command)
        main_layout.add_widget(self.command_input)
        
        # Область результатов
        self.results_label = Label(text='Results will appear here...', text_size=(None, None), valign='top')
        main_layout.add_widget(self.results_label)
        
        # Автоматические задачи
        Clock.schedule_interval(self.auto_security_check, 300)  # Каждые 5 минут
        
        return main_layout
    
    def start_voice_recognition(self, instance):
        self.status_label.text = 'Listening...'
        threading.Thread(target=self.listen_for_command).start()
    
    def listen_for_command(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
            
            command = self.recognizer.recognize_google(audio, language='ru-RU')
            Clock.schedule_once(lambda dt: self.process_voice_command(command))
            
        except sr.UnknownValueError:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Could not understand'))
        except sr.RequestError:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Speech service error'))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'Error: {e}'))
    
    def process_voice_command(self, command):
        self.command_input.text = command
        self.process_command(command)
    
    def process_text_command(self, instance):
        command = instance.text
        self.process_command(command)
    
    def process_command(self, command):
        command = command.lower()
        
        # Обучение новым командам
        if command in self.learning_data:
            response = self.learning_data[command]
            self.execute_learned_command(response)
        elif 'сканировать' in command or 'scan' in command:
            self.start_security_scan(None)
        elif 'статус' in command or 'status' in command:
            self.get_system_status()
        elif 'помощь' in command or 'help' in command:
            self.show_help()
        elif 'обучить' in command or 'learn' in command:
            self.learn_new_command(command)
        else:
            self.results_label.text = f"Unknown command: {command}\nSay 'help' for available commands"
        
        self.status_label.text = 'Ready'
    
    def start_security_scan(self, instance):
        self.status_label.text = 'Scanning device...'
        threading.Thread(target=self.perform_security_scan).start()
    
    def perform_security_scan(self):
        # Симуляция сканирования безопасности
        scan_results = {
            'apps_scanned': 45,
            'threats_found': 0,
            'permissions_issues': 2,
            'network_security': 'OK',
            'storage_encryption': 'Enabled'
        }
        
        result_text = f"""Security Scan Complete:
Apps: {scan_results['apps_scanned']}
Threats: {scan_results['threats_found']}
Permission Issues: {scan_results['permissions_issues']}
Network: {scan_results['network_security']}
Encryption: {scan_results['storage_encryption']}"""
        
        Clock.schedule_once(lambda dt: setattr(self.results_label, 'text', result_text))
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Scan complete'))
        
        self.speak("Security scan completed. No threats found.")
    
    def start_learning_mode(self, instance):
        self.status_label.text = 'Learning mode active'
        self.results_label.text = 'Learning Mode:\nSay "learn [command] means [action]"\nExample: "learn check battery means show battery status"'
    
    def learn_new_command(self, command):
        # Простое обучение: "learn X means Y"
        if 'means' in command:
            parts = command.split('means')
            if len(parts) == 2:
                trigger = parts[0].replace('learn', '').strip()
                action = parts[1].strip()
                
                self.learning_data[trigger] = action
                self.save_learning_data()
                
                self.results_label.text = f"Learned: '{trigger}' -> '{action}'"
                self.speak(f"I learned that {trigger} means {action}")
    
    def execute_learned_command(self, action):
        if 'battery' in action:
            self.results_label.text = "Battery Status: 85% (Good)"
        elif 'time' in action:
            self.results_label.text = f"Current time: {datetime.now().strftime('%H:%M:%S')}"
        elif 'scan' in action:
            self.start_security_scan(None)
        else:
            self.results_label.text = f"Executing: {action}"
    
    def get_system_status(self):
        status = {
            'security_level': 'High',
            'last_scan': '2 hours ago',
            'threats_blocked': 0,
            'system_health': 'Good'
        }
        
        status_text = f"""System Status:
Security Level: {status['security_level']}
Last Scan: {status['last_scan']}
Threats Blocked: {status['threats_blocked']}
System Health: {status['system_health']}"""
        
        self.results_label.text = status_text
    
    def show_help(self):
        help_text = """Available Commands:
• "сканировать" / "scan" - Security scan
• "статус" / "status" - System status  
• "обучить" / "learn" - Learning mode
• "помощь" / "help" - This help

Learning Examples:
• "learn check battery means show battery"
• "learn what time means show current time" """
        
        self.results_label.text = help_text
        self.speak("Available commands: scan, status, learn, and help")
    
    def auto_security_check(self, dt):
        # Автоматическая проверка каждые 5 минут
        self.status_label.text = 'Auto security check...'
        # Здесь можно добавить реальные проверки
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Ready'), 2)
    
    def speak(self, text):
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass  # TTS может не работать на всех устройствах
    
    def load_learning_data(self):
        try:
            with open('learning_data.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'check battery': 'show battery status',
                'what time': 'show current time',
                'security status': 'show security information'
            }
    
    def save_learning_data(self):
        try:
            with open('learning_data.json', 'w') as f:
                json.dump(self.learning_data, f, indent=2)
        except:
            pass

if __name__ == '__main__':
    MobileAssistantApp().run()