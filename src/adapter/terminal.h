#include <iostream>
#include <optional>
#include <ostream>
#include <sstream>

#include "canvas.h"
#include "display.h"

namespace Infomate::adapter {

struct Pixel {
    uint8_t r, g, b;
};

inline std::ostream& operator<<(std::ostream& os, const Pixel& p) {
    return (os << "\033[48;2;" << (int)p.r << ';' << (int)p.g << ';' << (int)p.b << "m  ");
}

class TerminalCanvas : public rgb_matrix::Canvas {
   public:
    TerminalCanvas() : buffer(width() * height()) {}

    int width() const override { return 64; }
    int height() const override { return 32; }

    void SetPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b) override {
        if (x < 0 || x >= width() || y < 0 || y >= height()) return;

        buffer[y * width() + x] = Pixel{r, g, b};
    };

    void Clear() override { Fill(0, 0, 0); }

    void Fill(uint8_t r, uint8_t g, uint8_t b) override {
        std::fill(buffer.begin(), buffer.end(), Pixel{r, g, b});
    };

    const std::optional<Pixel> at(int x, int y) const {
        if (x < 0 || x >= width() || y < 0 || y >= height()) return std::nullopt;

        return buffer[y * width() + x];
    }

   private:
    std::vector<Pixel> buffer;
};

class TerminalAdapter : public port::DisplayPort {
   public:
    TerminalAdapter() : canvas() {}

    void shutdown() override { std::cout << "\033[?25h\033[0m\n"; }

    rgb_matrix::Canvas* getCanvas() override { return &canvas; }

    void present() override {
        const std::string white = "\033[48;2;255;255;255m";
        const std::string reset = "\033[0m";
        const std::string border = white + std::string((canvas.width() + 2) * 2, ' ') + reset;

        std::ostringstream out;

        out << border + "\n";

        for (int y = 0; y < canvas.height(); y++) {
            out << white << "  ";

            for (int x = 0; x < canvas.width(); x++) {
                out << *canvas.at(x, y);
            }

            out << reset << white << "  " << reset << "\n";
        }

        out << border + "\n";
        std::cout << out.str() << std::flush;
    };

   private:
    TerminalCanvas canvas;
};

}  // namespace Infomate::adapter
