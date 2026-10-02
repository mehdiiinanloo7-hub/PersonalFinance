[app]
title = Personal Finance
package.name = personalfinance
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,txt
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
