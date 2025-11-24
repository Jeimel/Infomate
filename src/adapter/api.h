#include <crow.h>

#include "app.h"
#include "input.h"
#include "manager.h"
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

class CrowAdapter : public port::InputPort {
   public:
    CrowAdapter(AppManager& manager, int port) : port::InputPort(manager), port(port) {
        CROW_ROUTE(app, "/status").methods(crow::HTTPMethod::Get)([&manager] {
            // clang-format off
            return crow::json::wvalue(
                {{"version", INFOMATE_VERSION},
                {"app", manager.current()},
                {"brightness", manager.getBrightness()}
            });
            // clang-format on
        });

        CROW_ROUTE(app, "/app").methods(crow::HTTPMethod::Get)([]() {
            auto apps = app::AppRegistry::instance().list();
            crow::json::wvalue res;

            for (size_t i = 0; i < apps.size(); i++) res[i] = apps[i];

            return res;
        });

        CROW_ROUTE(app, "/app/deploy/<string>")
            .methods(crow::HTTPMethod::Post)([&manager](const std::string& appId) {
                return manager.swap(appId) ? crow::response(200) : error(404, "App not found!");
            });

        CROW_ROUTE(app, "/configure")
            .methods(crow::HTTPMethod::Post)([&manager](const crow::request& req) {
                auto body = crow::json::load(req.body);
                if (!body) return error(400, "Invalid JSON");

                return manager.configure(buildConfig(body)) ? crow::response(200)
                                                            : error(400, "Invalid Argument.");
            });

        CROW_ROUTE(app, "/brightness").methods(crow::HTTPMethod::Get)([&manager] {
            return crow::json::wvalue({{"brightness", manager.getBrightness()}});
        });

        CROW_ROUTE(app, "/brightness/<int>").methods(crow::HTTPMethod::Post)([&manager](int app) {
            manager.setBrightness(static_cast<int>(app));
            return crow::response(200);
        });
    }

    ~CrowAdapter() { stop(); }

    void run() override { app.port(port).signal_clear().loglevel(crow::LogLevel::Critical).run(); }

    void stop() override { app.stop(); }

   private:
    crow::SimpleApp app;

    int port;
};

}  // namespace Infomate::adapter
