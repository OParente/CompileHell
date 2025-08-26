# Diretórios
SRC_DIR = engine_src
ENGINE_DIR = engine
BUILD_DIR = build

# Detecta SO
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LIB_LINUX = $(BUILD_DIR)/libcompilehell.dylib
else
    LIB_LINUX = $(BUILD_DIR)/libcompilehell.so
endif
LIB_WINDOWS = $(BUILD_DIR)/compilehell.dll

# Compiladores
CC_LINUX = gcc
CC_WINDOWS = x86_64-w64-mingw32-gcc

# Flags
CFLAGS = -O2 -Wall -shared -fPIC
LIBS_LINUX = -lSDL2 -lSDL2_image -lSDL2_ttf
LIBS_WINDOWS = -lmingw32 -lSDL2main -lSDL2 -lSDL2_image

SRC = $(SRC_DIR)/compilehell.c

# Alvo padrão: build Linux e Windows
all: linux windows

# Build Linux
linux:
	@echo "Compilando para Linux/macOS..."
	@mkdir -p $(BUILD_DIR)
	$(CC_LINUX) $(CFLAGS) $(SRC) $(LIBS_LINUX) -o $(LIB_LINUX)
	@cp $(LIB_LINUX) $(ENGINE_DIR)/

# Build Windows
windows:
	@echo "Compilando para Windows (DLL)..."
	@mkdir -p $(BUILD_DIR)
	$(CC_WINDOWS) $(CFLAGS) $(SRC) $(LIBS_WINDOWS) -o $(LIB_WINDOWS)
	@cp $(LIB_WINDOWS) $(ENGINE_DIR)/

# Limpeza
clean:
	@echo "Removendo builds..."
	rm -rf $(BUILD_DIR)
	rm -f $(ENGINE_DIR)/libcompilehell.so
	rm -f $(ENGINE_DIR)/libcompilehell.dylib
	rm -f $(ENGINE_DIR)/compilehell.dll

.PHONY: all linux windows clean
