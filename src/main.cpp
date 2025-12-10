#include <csignal>
#include <cstring>
#include <thread>

#include "adapter/api.h"
#include "apps.h"
#include "manager.h"

#ifdef USE_RGB_MATRIX
#include "adapter/matrix.h"
#else
#include "adapter/terminal.h"
#endif

int main() {
    const int apiPort = 18080;
    const std::string initialApp = "clock";

#ifdef USE_RGB_MATRIX
    auto display = std::make_unique<Infomate::adapter::MatrixAdapter>();
#else
    auto display = std::make_unique<Infomate::adapter::TerminalAdapter>();
#endif

    Infomate::AppManager manager(std::move(display));

    Infomate::adapter::CrowAdapter api(manager, apiPort);
    auto api_thread = std::jthread([&api]() { api.run(); });

    manager.swap(initialApp);

    manager.run();

    manager.stop();
    api.stop();

    return 0;
}
