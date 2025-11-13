BUILD_DIR = build
TARGET = infomate

.PHONY: all run clean rebuild

all:
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && cmake .. > /dev/null
	@cmake --build $(BUILD_DIR) --target $(TARGET)

run: all
	@./$(BUILD_DIR)/$(TARGET)

clean:
	@rm -rf $(BUILD_DIR)

rebuild: clean all
