#include <ctime>
#include <filesystem>
#include <iterator>

#include "app.h"
#include "canvas.h"
#include "graphics.h"
#include "registry.h"

namespace Infomate::app::dvd {

class DVD : public App {
   public:
    DVD() : font() {
        std::filesystem::path path = std::filesystem::path(FONT_DIR) / "7x13.bdf";

        if (!font.LoadFont(path.string().c_str())) {
            throw 1;
        }

        x = random() % 64;
        y = random() % 32;
    }

    std::string getId() const override { return "dvd"; }
    std::string getName() const override { return "DVD"; }
    std::string getDescription() const override { return "Displays bouncing DVD logo"; }

    int update(rgb_matrix::Canvas* canvas) override {
        x += velX;
        y += velY;

        if (x + width >= canvas->width() || x <= 0) {
            x = std::max(0, std::min(x, canvas->width()));
            velX = -velX;

            changeColor();
        }

        if (y >= canvas->height() || y - height <= 0) {
            y = std::max(height, std::min(y, canvas->height()));
            velY = -velY;

            changeColor();
        }

        DrawText(canvas, font, x, y, colors[current], nullptr, "dvd");

        return 150;
    }

   private:
    void changeColor() { current = (current + 1) % std::size(colors); }

    rgb_matrix::Font font;

    rgb_matrix::Color colors[6] = {
        rgb_matrix::Color(0, 238, 255), rgb_matrix::Color(255, 119, 0),
        rgb_matrix::Color(0, 34, 255),  rgb_matrix::Color(255, 34, 0),
        rgb_matrix::Color(255, 0, 136), rgb_matrix::Color(187, 0, 255),
    };

    int x, y;
    int velX = 2, velY = 2;
    int width = 21, height = 9;
    int current = 0;
};

REGISTER_APP(DVD);

}  // namespace Infomate::app::dvd
