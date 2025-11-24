#include <ctime>
#include <filesystem>

#include "app.h"
#include "canvas.h"
#include "graphics.h"
#include "registry.h"

namespace Infomate::app::clock {

class Clock : public App {
   public:
    Clock() : font(), white(255, 255, 255) {
        std::filesystem::path path = std::filesystem::path(FONT_DIR) / "7x13.bdf";

        if (!font.LoadFont(path.string().c_str())) {
            throw 1;
        }
    }

    std::string getId() const override { return "clock"; }
    std::string getName() const override { return "Digital Clock"; }
    std::string getDescription() const override { return "Displays current time"; }

    int update(rgb_matrix::Canvas* canvas) override {
        std::time_t time = std::time(nullptr);
        std::tm local = *std::localtime(&time);

        char buffer[10];
        std::strftime(buffer, sizeof(buffer), "%H:%M", &local);

        DrawText(canvas, font, 12, 20, white, nullptr, buffer);

        return 1000 * (60 - local.tm_sec);
    }

   private:
    rgb_matrix::Font font;
    rgb_matrix::Color white;
};

REGISTER_APP(Clock);

}  // namespace Infomate::app::clock
