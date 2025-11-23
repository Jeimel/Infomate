#include <condition_variable>
#include <memory>
#include <mutex>

#include "app.h"
#include "port.h"

namespace Infomate {

class AppManager : public port::InputPort {
   public:
    explicit AppManager(std::unique_ptr<port::DisplayPort> display)
        : display(std::move(display)), running(false), brightness(100) {}

    ~AppManager() { stop(); }

    void run();
    void stop();

    bool swap(const std::string& appId) override;
    bool configure(const app::ConfigMap& config) override;
    std::string current() const override;

    int getBrightness() const override { return brightness; }
    void setBrightness(int b) override { brightness = std::clamp(b, 0, 100); }

   private:
    std::unique_ptr<port::DisplayPort> display;
    std::unique_ptr<app::App> app;

    std::condition_variable cv;
    mutable std::mutex mutex;

    std::atomic<bool> running;
    std::atomic<bool> changed;

    std::atomic<int> brightness;
};

}  // namespace Infomate
