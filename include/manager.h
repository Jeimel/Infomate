#pragma once

#include <condition_variable>
#include <memory>
#include <mutex>

#include "app.h"
#include "display.h"

namespace Infomate {

class AppManager {
   public:
    AppManager(std::unique_ptr<port::DisplayPort> display)
        : display(std::move(display)), running(false), brightness(100) {}

    ~AppManager() { stop(); }

    void run();
    void stop();

    bool swap(const std::string& appId);
    bool configure(const app::ConfigMap& config);
    std::string current() const;

    int getBrightness() const { return brightness; }
    void setBrightness(int b) { brightness = std::clamp(b, 0, 100); }

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
