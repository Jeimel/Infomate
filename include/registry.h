#pragma once

#include <functional>
#include <memory>
#include <mutex>
#include <vector>

#include "app.h"

namespace Infomate::app {

using AppFactory = std::function<std::unique_ptr<App>()>;

class AppRegistry {
   public:
    static AppRegistry& instance() {
        static AppRegistry registry;
        return registry;
    }

    void record(const std::string& id, AppFactory factory) {
        std::lock_guard<std::mutex> lock(mutex);

        factories[id] = std::move(factory);
    }

    std::unique_ptr<App> create(const std::string& id) const {
        std::lock_guard<std::mutex> lock(mutex);

        auto it = factories.find(id);
        if (it != factories.end()) {
            return it->second();
        }

        return nullptr;
    }

    bool exists(const std::string& id) const {
        std::lock_guard<std::mutex> lock(mutex);

        return factories.find(id) != factories.end();
    }

    size_t count() const {
        std::lock_guard<std::mutex> lock(mutex);

        return factories.size();
    }

    std::vector<std::string> list() const {
        std::lock_guard<std::mutex> lock(mutex);

        std::vector<std::string> ids;
        ids.reserve(factories.size());

        for (const auto& [id, _] : factories) {
            ids.push_back(id);
        }

        return ids;
    }

   private:
    AppRegistry() = default;
    AppRegistry(const AppRegistry&) = delete;

    AppRegistry& operator=(const AppRegistry&) = delete;

    mutable std::mutex mutex;
    std::unordered_map<std::string, AppFactory> factories;
};

#define REGISTER_APP(AppClass)                                                  \
    namespace {                                                                 \
    static bool _registered_##AppClass = []() {                                 \
        ::Infomate::app::AppRegistry::instance().record(                        \
            AppClass().getId(), []() { return std::make_unique<AppClass>(); }); \
        return true;                                                            \
    }();                                                                        \
    }

}  // namespace Infomate::app
