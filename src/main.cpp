#include <csignal>
#include <cstring>
#include <thread>

#include "adapter/api.h"
#include "adapter/terminal.h"
#include "apps.h"
#include "manager.h"

int main() {
    const int apiPort = 18080;
    const std::string initialApp = "dvd";

    auto display = std::make_unique<Infomate::adapter::TerminalAdapter>();

    Infomate::AppManager manager(std::move(display));
    Infomate::adapter::CrowAdapter api(manager, apiPort);

    auto api_thread = std::jthread([&api]() { api.run(); });

    manager.swap(initialApp);

    manager.run();

    manager.stop();
    api.stop();

    return 0;
}
