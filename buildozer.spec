[app]

# (str) Title of your application
title = Banana Leaf Disease Scanner

# (str) Package name
package.name = bananadisease

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ado

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,tflite

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3==3.10.10,kivy==2.3.1,tensorflow==2.13.0,pillow,numpy,tflite_runtime

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Android SDK version to use
android.sdk = 28

# (int) Android API to use
android.api = 28

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android architecture to build for
android.arch = armeabi-v7a

# (str) Main application file
main.py = test.py

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
