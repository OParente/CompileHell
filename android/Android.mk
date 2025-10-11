LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := compilehell
LOCAL_SRC_FILES := ../engine_src/compilehell.c main.cpp
LOCAL_LDLIBS := -landroid -llog
include $(BUILD_SHARED_LIBRARY)
