from api.base import Base
from api.routes.apps import ENV_PATH
from rgbmatrix import FrameCanvas

from sys import maxsize
from base64 import b64encode
from time import time
from requests import get, post
from dotenv import set_key, load_dotenv
from os import getenv, environ
from PIL import Image
from io import BytesIO


AUTH_URL = "https://accounts.spotify.com/api/token"
PLAYBACK_URL = "https://api.spotify.com/v1/me/player"


class Spotify(Base):
    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)

        code = getenv("SPOTIFY_AUTHORIZATION_CODE")
        if code:
            self._exchange_token(code)

    def _is_expired(self) -> bool:
        return int(getenv("SPOTIFY_EXPIRES_AT", default="0")) <= int(time())

    def _exchange_token(self, code: str) -> None:
        auth_code = b64encode(
            "{}:{}".format(
                getenv("SPOTIFY_CLIENT_ID"), getenv("SPOTIFY_CLIENT_SECRET")
            ).encode("utf-8")
        ).decode("utf-8")

        self._request(
            AUTH_URL,
            {
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": getenv("SPOTIFY_REDIRECT_URI"),
            },
            {
                "Authorization": "Basic " + auth_code,
            },
        )

        set_key(
            dotenv_path=ENV_PATH,
            key_to_set="SPOTIFY_AUTHORIZATION_CODE",
            value_to_set="",
        )
        environ["SPOTIFY_AUTHORIZATION_CODE"] = ""

    def _refresh_token(self) -> None:
        self._request(
            AUTH_URL,
            {
                "grant_type": "refresh_token",
                "client_id": getenv("SPOTIFY_CLIENT_ID"),
                "refresh_token": getenv("SPOTIFY_REFRESH_TOKEN"),
            },
        )

    def _request(self, url: str, data: dict, headers: dict = {}) -> None:
        headers.update({"Content-Type": "application/x-www-form-urlencoded"})

        response = post(url, data=data, headers=headers)
        if response.status_code != 200:
            return

        response = response.json()

        expires_at = str(int(time()) + response["expires_in"])

        set_key(
            dotenv_path=ENV_PATH,
            key_to_set="SPOTIFY_ACCESS_TOKEN",
            value_to_set=response["access_token"],
        )
        set_key(
            dotenv_path=ENV_PATH,
            key_to_set="SPOTIFY_REFRESH_TOKEN",
            value_to_set=response["refresh_token"],
        )
        set_key(
            dotenv_path=ENV_PATH,
            key_to_set="SPOTIFY_EXPIRES_AT",
            value_to_set=expires_at,
        )

        environ["SPOTIFY_ACCESS_TOKEN"] = response["access_token"]
        environ["SPOTIFY_REFRESH_TOKEN"] = response["refresh_token"]
        environ["SPOTIFY_EXPIRES_AT"] = expires_at

    def run(self) -> bool:
        if self._is_expired():
            self._refresh_token()

        response = get(
            PLAYBACK_URL,
            headers={
                "Authorization": "Bearer {}".format(getenv("SPOTIFY_ACCESS_TOKEN"))
            },
        )

        if response.status_code != 200:
            return False

        response = response.json()

        image_min = min(response["item"]["images"], key=lambda img: img["width"])
        image_data = get(image_min["url"]).content
        image = Image.open(BytesIO(image_data)).convert("RGB").resize((16, 16))

        name = response["item"]["name"]
        artist = response["item"]["album"]["artists"][0]["name"]

        return True

    @staticmethod
    def env() -> bool:
        return True

    @staticmethod
    def variables() -> list:
        return [
            "CLIENT_ID",
            "CLIENT_SECRET",
            "AUTHORIZATION_CODE",
            "REFRESH_TOKEN",
            "ACCESS_TOKEN",
            "EXPIRES_AT",
            "REDIRECT_URI",
        ]
