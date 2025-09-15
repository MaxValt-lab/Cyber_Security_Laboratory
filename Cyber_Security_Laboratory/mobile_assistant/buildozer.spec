[app]
title = CyberSec Mobile Assistant
package.name = cybersecassistant
package.domain = org.cybersec.assistant

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,kivymd,requests,speechrecognition,pyttsx3,pyaudio

[buildozer]
log_level = 2

android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,CAMERA

android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

[buildozer]
warn_on_root = 1