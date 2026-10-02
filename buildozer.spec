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

[app:android]

android.api = 33
android.minapi = 24
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1

p4a.branch = develop
p4a.commit = d2ee8c5
