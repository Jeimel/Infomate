#pragma once

#include "manager.h"

namespace Infomate::port {

class InputPort {
   public:
    InputPort(AppManager& manager) : manager(manager) {}
    virtual ~InputPort() = default;

    virtual void run() = 0;

    virtual void stop() = 0;

   protected:
    AppManager& manager;
};

}  // namespace Infomate::port
