[app]
title = Echographie Naye
package.name = echographienaye
package.domain = org.naye
source.dir =.
source.include_exts = py,kv,db,png,jpg,ttf
version = 1.0
requirements = python3,kivy,sqlite3
orientation = portrait
android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.logcat_filters = *:S python:D
[buildozer]
log_level = 2
warn_on_root = 1