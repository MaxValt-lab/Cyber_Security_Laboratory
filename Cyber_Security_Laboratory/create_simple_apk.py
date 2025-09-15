#!/usr/bin/env python3
"""
Создание простого APK без сложных зависимостей
"""
import os
import zipfile
import json
from pathlib import Path

def create_android_manifest():
    """Создание AndroidManifest.xml"""
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.cyberseclab.app"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:label="Cyber Security Lab"
        android:icon="@drawable/icon"
        android:theme="@android:style/Theme.NoTitleBar">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    return manifest

def create_main_activity():
    """Создание MainActivity.java"""
    activity = '''package org.cyberseclab.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;

public class MainActivity extends Activity {
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        webView = new WebView(this);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("file:///android_asset/index.html");
        
        setContentView(webView);
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}'''
    return activity

def create_web_interface():
    """Создание веб-интерфейса для APK"""
    html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Security Lab</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
        .container { max-width: 400px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .form { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .input-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #3498db; color: white; border: none; border-radius: 4px; font-size: 16px; margin: 10px 0; }
        button:hover { background: #2980b9; }
        .response { background: #ecf0f1; padding: 15px; border-radius: 4px; margin: 10px 0; min-height: 50px; }
        .status { padding: 10px; border-radius: 4px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Cyber Security Lab</h1>
            <p>Mobile Security Monitor</p>
        </div>
        
        <div class="form">
            <div class="input-group">
                <label>Server URL:</label>
                <input type="text" id="serverUrl" value="http://192.168.1.100:8000" placeholder="Server address">
            </div>
            
            <div class="input-group">
                <label>Event Type:</label>
                <select id="eventType">
                    <option value="mobile_event">Mobile Event</option>
                    <option value="login_attempt">Login Attempt</option>
                    <option value="file_access">File Access</option>
                    <option value="network_scan">Network Scan</option>
                </select>
            </div>
            
            <div class="input-group">
                <label>Severity:</label>
                <select id="severity">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                </select>
            </div>
            
            <div class="input-group">
                <label>Message:</label>
                <input type="text" id="message" value="Mobile security event" placeholder="Event description">
            </div>
            
            <button onclick="sendEvent()">Send Event</button>
            <button onclick="checkStatus()">Check Status</button>
            <button onclick="getStats()">Get Statistics</button>
        </div>
        
        <div id="response" class="response">Ready to send events...</div>
    </div>

    <script>
        async function sendEvent() {
            const serverUrl = document.getElementById('serverUrl').value;
            const eventData = {
                type: document.getElementById('eventType').value,
                source: 'mobile',
                severity: document.getElementById('severity').value,
                message: document.getElementById('message').value
            };
            
            try {
                const response = await fetch(serverUrl + '/api/event', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(eventData)
                });
                
                const result = await response.json();
                showResponse(`Event sent! Risk: ${result.risk_score}, Action: ${result.action}`, 'success');
            } catch (error) {
                showResponse(`Error: ${error.message}`, 'error');
            }
        }
        
        async function checkStatus() {
            const serverUrl = document.getElementById('serverUrl').value;
            
            try {
                const response = await fetch(serverUrl + '/api/status');
                const result = await response.json();
                showResponse(`Server status: ${result.status}`, 'success');
            } catch (error) {
                showResponse(`Error: ${error.message}`, 'error');
            }
        }
        
        async function getStats() {
            const serverUrl = document.getElementById('serverUrl').value;
            
            try {
                const response = await fetch(serverUrl + '/api/stats');
                const result = await response.json();
                showResponse(`Stats - Events: ${result.total_events}, Incidents: ${result.total_incidents}, Avg Risk: ${result.average_risk_score}`, 'success');
            } catch (error) {
                showResponse(`Error: ${error.message}`, 'error');
            }
        }
        
        function showResponse(message, type) {
            const responseDiv = document.getElementById('response');
            responseDiv.textContent = message;
            responseDiv.className = 'response ' + type;
        }
    </script>
</body>
</html>'''
    return html

def create_apk_structure():
    """Создание структуры APK"""
    print("[STEP] Создание структуры APK...")
    
    # Создание директорий
    apk_dir = Path("apk_build")
    if apk_dir.exists():
        import shutil
        shutil.rmtree(apk_dir)
    
    dirs = [
        "apk_build/src/main/java/org/cyberseclab/app",
        "apk_build/src/main/assets",
        "apk_build/src/main/res/drawable",
        "apk_build/src/main/res/values"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Создание файлов
    files = {
        "apk_build/src/main/AndroidManifest.xml": create_android_manifest(),
        "apk_build/src/main/java/org/cyberseclab/app/MainActivity.java": create_main_activity(),
        "apk_build/src/main/assets/index.html": create_web_interface(),
    }
    
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("[OK] Структура APK создана")
    return apk_dir

def create_gradle_build():
    """Создание build.gradle"""
    gradle = '''apply plugin: 'com.android.application'

android {
    compileSdkVersion 31
    
    defaultConfig {
        applicationId "org.cyberseclab.app"
        minSdkVersion 21
        targetSdkVersion 31
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.4.0'
}'''
    return gradle

def main():
    """Основная функция создания APK"""
    print("=" * 50)
    print("Создание простого APK")
    print("=" * 50)
    
    try:
        apk_dir = create_apk_structure()
        
        # Создание build.gradle
        with open(apk_dir / "build.gradle", "w") as f:
            f.write(create_gradle_build())
        
        print("\n[SUCCESS] Структура APK создана!")
        print(f"Директория: {apk_dir}")
        print("\nДля сборки APK:")
        print("1. Установите Android Studio")
        print("2. Откройте проект в apk_build/")
        print("3. Выполните Build -> Build APK")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка создания APK: {e}")
        return False

if __name__ == "__main__":
    main()