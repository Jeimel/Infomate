#pragma once

#include <string>

#include "app.h"
#include "canvas.h"

namespace Infomate::port {

class DisplayPort {
   public:
    virtual ~DisplayPort() = default;

    virtual void shutdown() = 0;

    virtual rgb_matrix::Canvas* getCanvas() = 0;

    virtual void present() = 0;
};

class InputPort {
   public:
    virtual ~InputPort() = default;

    virtual bool swap(const std::string& appId) = 0;
    virtual bool configure(const app::ConfigMap& config) = 0;
    virtual std::string current() const = 0;

    virtual void setBrightness(int brightness) = 0;
    virtual int getBrightness() const = 0;
};

}  // namespace Infomate::port
