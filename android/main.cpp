#include <jni.h>
#include <android/log.h>
#include <Python.h>

#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, "CompileHell", __VA_ARGS__)

extern "C" void engine_main_from_python(); // placeholder if you want to call into libcompilehell

// ANativeActivity onCreate entrypoint - called by Android for NativeActivity apps
extern "C" void ANativeActivity_onCreate(struct ANativeActivity* activity,
                                        void* savedState, size_t savedStateSize) {
    LOGI("CompileHell native onCreate start");

    // Initialize Python interpreter
    Py_Initialize();

    // Add path to assets py directory - adjust this path depending on packaging (example location)
    PyRun_SimpleString("import sys, os");
    PyRun_SimpleString("sys.path.append('/data/data/org.compilehell/files/app/py')");

    LOGI("Executing game.main()");
    PyRun_SimpleString("import game; game.main()");

    Py_Finalize();
    LOGI("CompileHell native onCreate end");
}
