#include <crow.h>

#include "app.h"
#include "port.h"
#include "registry.h"

namespace Infomate::adapter {

inline crow::response error(int code, const std::string& msg) {
    return crow::response(code, crow::json::wvalue({{"error", msg}}));
}

inline app::ConfigMap buildConfig(crow::json::rvalue& body) {
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

    return config;
}

class CrowAdapter {
   public:
    CrowAdapter(port::InputPort& port, int serverPort) : port(port), serverPort(serverPort) {
        CROW_ROUTE(app, "/status")
        ([&port] {
            return crow::json::wvalue(
                {{"app", port.current()}, {"brightness", port.getBrightness()}});
        });

        CROW_ROUTE(app, "/app")
        ([] {
            auto apps = app::AppRegistry::instance().list();
            crow::json::wvalue res;

            for (size_t i = 0; i < apps.size(); i++) res[i] = apps[i];

            return res;
        });

        CROW_ROUTE(app, "/app/<string>")
            .methods(crow::HTTPMethod::POST)([&port](const std::string& appId) {
                if (port.swap(appId)) return crow::response(200);
                return error(404, "App not found: " + appId);
            });

        CROW_ROUTE(app, "/brightness")
        ([&port] { return crow::json::wvalue({{"brightness", port.getBrightness()}}); });

        CROW_ROUTE(app, "/brightness")
            .methods(crow::HTTPMethod::POST)([&port](const crow::request& req) {
                auto body = crow::json::load(req.body);
                if (!body || !body.has("value")) return error(400, "Missing 'value' field");

                port.setBrightness(static_cast<int>(body["value"].i()));
                return crow::response(200);
            });

        CROW_ROUTE(app, "/configure")
            .methods(crow::HTTPMethod::POST)([&port](const crow::request& req) {
                auto body = crow::json::load(req.body);
                if (!body) return error(400, "Invalid JSON");

                if (port.configure(buildConfig(body))) return crow::response(200);
                return error(400, "No active app");
            });
    }

    ~CrowAdapter() { stop(); }

    void run() { app.port(serverPort).signal_clear().loglevel(crow::LogLevel::Critical).run(); }

    void stop() { app.stop(); }

   private:
    port::InputPort& port;

    crow::SimpleApp app;
    int serverPort;
};

}  // namespace Infomate::adapter
