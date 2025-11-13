BUILD_DIR = build
TARGET = infomate

.PHONY: all run clean rebuild

all:
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .. > /dev/null
	@cmake --build $(BUILD_DIR) --target $(TARGET)

run: all
	@./$(BUILD_DIR)/$(TARGET)

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f compile_commands.json

rebuild: clean all

