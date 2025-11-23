#pragma once

#include "manager.h"

namespace Infomate::port {

class InputPort {
   public:
    InputPort(AppManager& manager) : manager(manager) {}
    virtual ~InputPort() = default;

   protected:
    AppManager& manager;
};

}  // namespace Infomate::port
