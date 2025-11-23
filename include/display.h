#pragma once

#include "canvas.h"

namespace Infomate::port {

class DisplayPort {
   public:
    virtual ~DisplayPort() = default;

    virtual void shutdown() = 0;

    virtual rgb_matrix::Canvas* getCanvas() = 0;

    virtual void present() = 0;
};

}  // namespace Infomate::port
