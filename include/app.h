#pragma once

#include <any>
#include <string>
#include <unordered_map>

#include "canvas.h"

namespace Infomate::app {

using ConfigMap = std::unordered_map<std::string, std::any>;

class App {
   public:
    virtual ~App() = default;

    virtual std::string getId() const = 0;
    virtual std::string getName() const = 0;
    virtual std::string getDescription() const { return ""; };

    virtual int update(rgb_matrix::Canvas* c) = 0;

    virtual void configure(const ConfigMap& config) {}
};

}  // namespace Infomate::app
