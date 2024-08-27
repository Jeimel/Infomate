# Infomate
Infomate (*info*rmation and auto*mate*) is an API, which itself is connected to a led-matrix. In this way controlling the display can be done using different graphical or command-line interfaces, but also by creating API calls in e.g. Apple Shortcuts. The API offers different applications (see [Apps](#Apps)), which will be rendered on the matrix.

## Documentation
Thanks to FastAPI automated docs, either Swagger UI or ReDoc, are generated at runtime.

## Apps
Apps are stored in the repository and can be deployed through the API. A list of all available apps with a short description and an id can also be fetched.

## Installation
```shell
git clone https://github.com/Jeimel/Infomate
cd Infomate && bash init.sh
```
