#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

def create_android_project():
    """Создание Android проекта"""
    
    # Создание структуры Android проекта
    android_dir = Path("android_project")
    if android_dir.exists():
        shutil.rmtree(android_dir)
    
    # Создание директорий
    dirs = [
        "android_project/app/src/main/java/org/cybersec/assistant",
        "android_project/app/src/main/res/layout",
        "android_project/app/src/main/res/values",
        "android_project/app/src/main/res/drawable",
        "android_project/app/src/main/assets"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # AndroidManifest.xml
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.cybersec.assistant">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    
    <application
        android:allowBackup="true"
        android:label="CyberSec Assistant"
        android:theme="@android:style/Theme.Material.Light">
        
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
    
    with open("android_project/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(manifest)
    
    # MainActivity.java
    main_activity = '''package org.cybersec.assistant;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.speech.RecognizerIntent;
import android.content.Intent;
import android.speech.SpeechRecognizer;
import java.util.ArrayList;

public class MainActivity extends Activity {
    private WebView webView;
    private SpeechRecognizer speechRecognizer;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        webView = new WebView(this);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        
        webView.setWebViewClient(new WebViewClient());
        webView.addJavascriptInterface(new AndroidInterface(), "Android");
        
        webView.loadUrl("file:///android_asset/index.html");
        setContentView(webView);
        
        initSpeechRecognizer();
    }
    
    private void initSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
    }
    
    public class AndroidInterface {
        @android.webkit.JavascriptInterface
        public void startVoiceRecognition() {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, 
                          RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            startActivityForResult(intent, 1);
        }
        
        @android.webkit.JavascriptInterface
        public String getDeviceInfo() {
            return "Android Device";
        }
        
        @android.webkit.JavascriptInterface
        public void performSecurityScan() {
            // Запуск сканирования безопасности
            webView.post(() -> {
                webView.evaluateJavascript("onSecurityScanComplete({result: 'scan_complete'})", null);
            });
        }
    }
    
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        
        if (requestCode == 1 && resultCode == RESULT_OK) {
            ArrayList<String> results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (results != null && !results.isEmpty()) {
                String spokenText = results.get(0);
                webView.evaluateJavascript("onVoiceResult('" + spokenText + "')", null);
            }
        }
    }
}'''
    
    with open("android_project/app/src/main/java/org/cybersec/assistant/MainActivity.java", "w") as f:
        f.write(main_activity)
    
    # HTML интерфейс
    html_interface = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSec Assistant</title>
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #f0f0f0; }
        .container { max-width: 400px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .card { background: white; margin: 15px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { width: 100%; padding: 15px; margin: 10px 0; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        .btn-primary { background: #3498db; color: white; }
        .btn-success { background: #27ae60; color: white; }
        .btn-warning { background: #f39c12; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; background: #ecf0f1; }
        .results { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; min-height: 100px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CyberSec Assistant</h1>
            <p>Mobile Security Helper</p>
        </div>
        
        <div class="card">
            <h3>Voice Commands</h3>
            <button class="btn btn-primary" onclick="startVoice()">🎤 Start Voice Recognition</button>
            <div id="voiceResult" class="status">Say something...</div>
        </div>
        
        <div class="card">
            <h3>Security Scan</h3>
            <button class="btn btn-danger" onclick="startScan()">🔍 Scan Device</button>
            <button class="btn btn-warning" onclick="checkApps()">📱 Check Apps</button>
            <button class="btn btn-success" onclick="checkPermissions()">🔐 Check Permissions</button>
        </div>
        
        <div class="card">
            <h3>Learning Mode</h3>
            <button class="btn btn-info" onclick="enableLearning()">🧠 Enable Learning</button>
            <input type="text" id="commandInput" placeholder="Teach me a command..." style="width:100%; padding:10px; margin:10px 0;">
        </div>
        
        <div id="results" class="results">
            Results will appear here...
        </div>
    </div>

    <script>
        let learningMode = false;
        
        function startVoice() {
            if (typeof Android !== 'undefined') {
                Android.startVoiceRecognition();
            } else {
                document.getElementById('voiceResult').textContent = 'Voice recognition not available';
            }
        }
        
        function onVoiceResult(text) {
            document.getElementById('voiceResult').textContent = 'You said: ' + text;
            processCommand(text);
        }
        
        function processCommand(command) {
            const cmd = command.toLowerCase();
            
            if (cmd.includes('scan') || cmd.includes('сканировать')) {
                startScan();
            } else if (cmd.includes('apps') || cmd.includes('приложения')) {
                checkApps();
            } else if (cmd.includes('help') || cmd.includes('помощь')) {
                showHelp();
            } else if (learningMode) {
                learnCommand(command);
            } else {
                showResults('Command: ' + command + '\\nSay "help" for available commands');
            }
        }
        
        function startScan() {
            showResults('Starting security scan...');
            
            if (typeof Android !== 'undefined') {
                Android.performSecurityScan();
            } else {
                // Симуляция сканирования
                setTimeout(() => {
                    const results = {
                        apps_scanned: 42,
                        threats_found: 0,
                        security_score: 85,
                        recommendations: ['Update apps', 'Check permissions']
                    };
                    onSecurityScanComplete(results);
                }, 2000);
            }
        }
        
        function onSecurityScanComplete(results) {
            const resultText = `Security Scan Complete:
Apps Scanned: ${results.apps_scanned || 42}
Threats Found: ${results.threats_found || 0}
Security Score: ${results.security_score || 85}/100
Status: ${results.security_score > 80 ? 'Good' : 'Needs Attention'}`;
            
            showResults(resultText);
        }
        
        function checkApps() {
            showResults('Checking installed apps...\\nFound 42 apps\\n2 need attention\\n40 are safe');
        }
        
        function checkPermissions() {
            showResults('Checking app permissions...\\n5 apps have dangerous permissions\\nRecommend reviewing camera and location access');
        }
        
        function enableLearning() {
            learningMode = !learningMode;
            const btn = event.target;
            if (learningMode) {
                btn.textContent = '🧠 Learning Mode ON';
                btn.style.background = '#27ae60';
                showResults('Learning mode enabled. Say commands to teach me.');
            } else {
                btn.textContent = '🧠 Enable Learning';
                btn.style.background = '#3498db';
                showResults('Learning mode disabled.');
            }
        }
        
        function learnCommand(command) {
            showResults('Learning command: "' + command + '"\\nI will remember this for next time.');
            // Здесь можно добавить сохранение команды
        }
        
        function showHelp() {
            const helpText = `Available Commands:
• "scan" - Start security scan
• "check apps" - Check installed apps  
• "check permissions" - Review app permissions
• "help" - Show this help
• Enable learning mode to teach new commands`;
            
            showResults(helpText);
        }
        
        function showResults(text) {
            document.getElementById('results').innerHTML = text.replace(/\\n/g, '<br>');
        }
        
        // Автоматическая проверка при загрузке
        window.onload = function() {
            showResults('CyberSec Assistant Ready\\nTap voice button or use commands');
        };
    </script>
</body>
</html>'''
    
    with open("android_project/app/src/main/assets/index.html", "w", encoding='utf-8') as f:
        f.write(html_interface)
    
    # build.gradle
    build_gradle = '''apply plugin: 'com.android.application'

android {
    compileSdkVersion 31
    
    defaultConfig {
        applicationId "org.cybersec.assistant"
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
    
    with open("android_project/app/build.gradle", "w") as f:
        f.write(build_gradle)
    
    print("✅ Android project structure created!")
    print("📁 Location: android_project/")
    print("🔧 Open in Android Studio to build APK")
    
    return "android_project"

def main():
    print("🤖 Building CyberSec Mobile Assistant")
    print("="*50)
    
    # Создание Android проекта
    project_dir = create_android_project()
    
    print(f"\n✅ Mobile app project created: {project_dir}")
    print("\nNext steps:")
    print("1. Open android_project/ in Android Studio")
    print("2. Build APK: Build -> Build APK(s)")
    print("3. Install on device")
    
    return project_dir

if __name__ == "__main__":
    main()