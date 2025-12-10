#include <canvas.h>
#include <led-matrix.h>

#include "display.h"

namespace Infomate::adapter {

class MatrixAdapter : public port::DisplayPort {
   public:
    MatrixAdapter() {
        rgb_matrix::RGBMatrix::Options options;
        options.hardware_mapping = "regular";
        options.rows = 32;
        options.cols = 64;
        options.chain_length = 1;
        options.parallel = 1;
        options.brightness = 100;
        options.show_refresh_rate = true;

        rgb_matrix::RuntimeOptions runtime;
        runtime.gpio_slowdown = 1;

        matrix = rgb_matrix::RGBMatrix::CreateFromOptions(options, runtime);
        if (matrix == NULL) throw 1;

        canvas = matrix->CreateFrameCanvas();

        canvas->Clear();
        present();
    }

    ~MatrixAdapter() { stop(); }

    void stop() override {
        matrix->Clear();
        delete matrix;
    }

    rgb_matrix::Canvas* getCanvas() override { return canvas; }

    void present() override { canvas = matrix->SwapOnVSync(canvas); }

   private:
    rgb_matrix::RGBMatrix* matrix;
    rgb_matrix::FrameCanvas* canvas;
};

}  // namespace Infomate::adapter
