#include "manager.h"

#include <atomic>
#include <chrono>
#include <mutex>

#include "app.h"
#include "registry.h"

using Infomate::AppManager;

void AppManager::run() {
    using clock = std::chrono::steady_clock;

    changed = false;
    running = true;

    while (running) {
        auto start = clock::now();
        int delay = 1000;

        {
            std::lock_guard<std::mutex> lock(mutex);

            changed = false;

            if (!app) {
                continue;
            }

            auto* canvas = display->getCanvas();
            canvas->Clear();

            delay = app->update(canvas);
            display->present();
        }

        auto target = std::chrono::milliseconds(delay);
        auto elapsed = clock::now() - start;

        if (elapsed >= target) {
            continue;
        }

        std::unique_lock<std::mutex> lock(mutex);
        cv.wait_for(lock, target - elapsed, [this] { return !running || changed; });
    }

    display->shutdown();
}

void AppManager::stop() {
    cv.notify_all();
    running = false;
}

bool AppManager::swap(const std::string& appId) {
    auto app = app::AppRegistry::instance().create(appId);
    if (!app) return false;

    {
        std::lock_guard<std::mutex> lock(mutex);
        this->app = std::move(app);
        changed = true;
    }

    cv.notify_all();
    return true;
}

bool AppManager::configure(const app::ConfigMap& config) {
    std::lock_guard<std::mutex> lock(mutex);

    if (!app) return false;

    app->configure(config);
    return true;
}

std::string AppManager::current() const {
    std::lock_guard<std::mutex> lock(mutex);

    return app ? app->getId() : "";
}
