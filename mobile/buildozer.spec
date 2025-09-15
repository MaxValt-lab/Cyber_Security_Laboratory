[app]
title = Cyber Security Lab
package.name = cyberseclab
package.domain = org.cyberseclab

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,kivymd,requests

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 31

[buildozer]
log_level = 2