#!/bin/bash
set -e
echo "This is a template build script. Edit ANDROID_NDK_HOME and ANDROID_SDK_ROOT at top if needed."
ANDROID_NDK_HOME="${ANDROID_NDK_HOME:-$HOME/Android/ndk}"
ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/Android}"
API=21
ABI=arm64-v8a

echo "1) Ensure ANDROID_NDK_HOME is set: $ANDROID_NDK_HOME"
echo "2) Ensure ANDROID_SDK_ROOT is set: $ANDROID_SDK_ROOT"
echo "3) This script will prepare pyc files and call gradle to assemble the APK."
echo "You still need to compile CPython for Android (see README) or use python-for-android."

# Prepare pyc
echo "Compiling Python files to bytecode..."
python3 -m compileall -q pyCompileHell game.py object_builder.py

# Copy compiled bytecode into android/assets/py
mkdir -p android/assets/py
find pyCompileHell -name '*.pyc' -exec cp {} android/assets/py/ \;
if [ -f game.pyc ]; then cp game.pyc android/assets/py/; fi
if [ -f object_builder.pyc ]; then cp object_builder.pyc android/assets/py/; fi
cp -r scenes android/assets/ || true

echo "Build script finished. Use the Android NDK to compile libcompilehell and package the APK."
echo "To build native library with ndk-build: cd android && $ANDROID_NDK_HOME/ndk-build NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=Android.mk APP_ABI=$ABI"
echo "Then use ./gradlew assembleDebug inside android/ to create an APK (you may need to tweak Gradle files)."
