#include <crow.h>

#include "app.h"
#include "input.h"
#include "manager.h"
#include "registry.h"

namespace Infomate::adapter {

inline crow::response error(int code, const std::string& msg) {
    return crow::response(code, crow::json::wvalue({{"error", msg}}));
}

class CrowAdapter : public port::InputPort {
   public:
    CrowAdapter(AppManager& manager, int serverPort)
        : port::InputPort(manager), serverPort(serverPort) {
        CROW_ROUTE(app, "/status")
        ([&manager] {
            return crow::json::wvalue(
                {{"app", manager.current()}, {"brightness", manager.getBrightness()}});
        });

        CROW_ROUTE(app, "/app")(handleApp);

        CROW_ROUTE(app, "/app/<string>")
            .methods(crow::HTTPMethod::POST)([&manager](const std::string& appId) {
                if (manager.swap(appId)) return crow::response(200);
                return error(404, "App not found: " + appId);
            });

        CROW_ROUTE(app, "/brightness")
        ([&manager] { return crow::json::wvalue({{"brightness", manager.getBrightness()}}); });

        CROW_ROUTE(app, "/brightness/<int>")
            .methods(crow::HTTPMethod::POST)([&manager](const int app) {
                manager.setBrightness(static_cast<int>(app));
                return crow::response(200);
            });

        CROW_ROUTE(app, "/configure")
            .methods(crow::HTTPMethod::POST)(
                [this](const crow::request& req) { return this->configure(req); });
    }

    ~CrowAdapter() { stop(); }

    void run() { app.port(serverPort).signal_clear().loglevel(crow::LogLevel::Critical).run(); }

    void stop() { app.stop(); }

   private:
    static crow::response handleApp() {
        auto apps = app::AppRegistry::instance().list();
        crow::json::wvalue res;

        for (size_t i = 0; i < apps.size(); i++) res[i] = apps[i];

        return res;
    }

    crow::response configure(const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body) return error(400, "Invalid JSON");

        app::ConfigMap config;

        for (const auto& key : body.keys()) {
            const auto& val = body[key];

            switch (val.t()) {
                case crow::json::type::Number:
                    config[key] = static_cast<int>(val.i());
                    break;
                case crow::json::type::String:
                    config[key] = std::string(val.s());
                    break;
                case crow::json::type::True:
                    config[key] = true;
                    break;
                case crow::json::type::False:
                    config[key] = false;
                    break;
                default:
                    break;
            }
        }

        if (manager.configure(config)) return crow::response(200);
        return error(400, "No active app");
    }

    crow::SimpleApp app;
    int serverPort;
};

}  // namespace Infomate::adapter
