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
android.sdk = 33

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK path (if empty, it will be automatically downloaded.)
android.ndk_path = /home/runner/Android/Sdk/ndk/25.2.9519653

# (str) Android SDK path (if empty, it will be automatically downloaded.)
android.sdk_path = /home/runner/Android/Sdk

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library sources for easier debugging
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a

# (str) The name of the Android keystore to use.
#android.keystore =

# (str) The storage for the Android keystore
#android.keystore.storage =

# (str) The alias for the Android keystore
#android.keystore.alias =

# (str) The key password for the Android keystore
#android.keystore.keypassword =

# (str) The keystore password for the Android keystore
#android.keystore.password =

# (str) The main activity class name.
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Extra java code to insert into AndroidManifest.xml
#android.extra_manifest_xml =

# (str) Extra xml to insert directly into AndroidManifest.xml
#android.extra_xml =

# (str) Override the app label
#android.app_label =

# (str) Override the process name
#android.process_name =

# (list) Permissions to grant (for example: ["android.permission.CAMERA"])
#android.grant_permissions =

# (int) Override the version code
#android.numeric_version = 1

# (str) Main activity class name
#android.mainactivity = "org.kivy.android.PythonActivity"

# (str) OUYA Console category
#android.ouya.category = GAME

# (str) Filename of your main.py
main.py = test.py

# (str) Filename of your app icon
#icon.filename = %(source.dir)s/data/icon.png

# (str) Filename of your app presplash
#presplash.filename = %(source.dir)s/data/presplash.png

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Display a warning if the application is being run in development mode
#warn_on_development = True

# (bool) Indicate if the application should be deployed in debug mode
#debug = False

# (bool) Allow running the application in the background
#background = False

# (bool) Preserve temporary files such as python bytecode
#preserve_temp = False

# (bool) Clear temporary files such as python bytecode
#clear_temp = True

# (str) Python for android branch to use
#p4a.branch = master

# (str) Oboe version to use
#oboe.version = 1.6.1

# (str) OpenAL version to use
#openal.version = 1.21.1

# (str) SDL2 version to use
#sdl2.version = 2.26.1

# (str) SDL2 image version to use
#sdl2.image.version = 2.6.2

# (str) SDL2 mixer version to use
#sdl2.mixer.version = 2.6.2

# (str) SDL2 ttf version to use
#sdl2.ttf.version = 2.20.2
