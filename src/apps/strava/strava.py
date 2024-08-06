from api.base import Base
from rgbmatrix import FrameCanvas, graphics

from requests import get, post
from datetime import datetime, timedelta
from time import strftime, gmtime, mktime
from PIL import Image
from io import BytesIO
from base64 import b64decode
from os import getenv, environ

STRAVA_URL = "https://www.strava.com/api/v3/athlete/activities"
AUTH_URL = "https://www.strava.com/api/v3/oauth/token"
STRAVA_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAACcAAAAIAgMAAAAHNw5FAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAJUExURQAAAPxMAv///9aHa3MAAAABdFJOUwBA5thmAAAAAWJLR0QCZgt8ZAAAAAd0SU1FB+gIBQ0pMrUk1YQAAAABb3JOVAHPoneaAAAARUlEQVQI1x3KsQ3AIBADQFN4gEj8PlB8byR7/1US0l1xqJ326N5ATjpjNwFhkjzNhaxLuRaoyVwK+uiyI+RjuR4Zde/PF5WTDvPa5x10AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTA4LTA1VDEzOjQxOjM0KzAwOjAwJtuDlQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wOC0wNVQxMzo0MTozNCswMDowMFeGOykAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDgtMDVUMTM6NDE6NTArMDA6MDAyszdiAAAAAElFTkSuQmCC"
RUNNER_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAYAAAD68A/GAAAAAXNSR0IArs4c6QAAAFtJREFUGFdjZMACKkM9/oOE21fvYIRJwxkwAZCinFAjMFc6rA27wqerqv6LL+qA28Gy5R8jSAykAcNEkKo/Pkxgq0EApBhEYyjEpghDodJGn//3/LeANSOzQXwArNUiByWbNhwAAAAASUVORK5CYII="
ROAD_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAYAAAD68A/GAAAAAXNSR0IArs4c6QAAAEtJREFUGFdjZCAAlDb6/L/nv4WREZ86kKK7fpsZlDf5MoAV/vFh+g+iWbb8Q9EIUggziBGkCKYAnQ1SpJbqxYDVanTTYZrxuhHZ/QAu5CRDAMtWogAAAABJRU5ErkJggg=="
CLOCK_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAYAAAD68A/GAAAAAXNSR0IArs4c6QAAAFtJREFUGFdjZEAC/////4/MZ2RkZITx4QyQor++zMjqGJg3/2WAKcZQyLLlH4ObmxtDXl4eg7e3N26FXr9cGHbWnICYbPsRu0KGw/wMWz8tY/Dmi8KtECSDzzMAbNosBwnLvJ4AAAAASUVORK5CYII="
FONT_NAME = "5x7"


class Strava(Base):
    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)
        self.font = Base.get_font(FONT_NAME)
        self.logo = Image.open(BytesIO(b64decode(STRAVA_IMAGE.encode()))).convert("RGB")
        self.clock = Image.open(BytesIO(b64decode(CLOCK_IMAGE.encode()))).convert("RGB")
        self.road = Image.open(BytesIO(b64decode(ROAD_IMAGE.encode()))).convert("RGB")
        self.runner = Image.open(BytesIO(b64decode(RUNNER_IMAGE.encode()))).convert(
            "RGB"
        )
        self.white = graphics.Color(255, 255, 255)
        self.client_id = getenv("CLIENT_ID")
        self.client_secret = getenv("CLIENT_SECRET")

        code = getenv("AUTHORIZATION_CODE")
        if code:
            self._exchange_token(code)
            del environ["AUTHORIZATION_CODE"], code

        self.expires_at = int(getenv("EXPIRES_AT", default="0"))
        self.refresh_token = getenv("REFRESH_TOKEN")
        if self._is_expired():
            self._refresh_token()
            return

        self.access_token = getenv("ACCESS_TOKEN")

    def _is_expired(self) -> bool:
        return self.expires_at <= int(datetime.now().timestamp())

    def _exchange_token(self, code: str) -> None:
        self._auth_request({
            "code": code,
            "grant_type": "authorization_code",
        })

    def _refresh_token(self) -> None:
        self._auth_request({
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        })

        self.expires_at = int(getenv("EXPIRES_AT", default="0"))
        self.refresh_token = getenv("REFRESH_TOKEN")
        self.access_token = getenv("ACCESS_TOKEN")

    def _auth_request(self, data: dict) -> None:
        response = post(AUTH_URL, data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }.update(data)).json()

        environ["ACCESS_TOKEN"] = response["access_token"]
        environ["REFRESH_TOKEN"] = response["refresh_token"]
        environ["EXPIRES_AT"] = response["expires_at"]

    def run(self) -> bool:
        if self._is_expired():
            self._refresh_token()

        now = datetime.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        response = get(
            url=STRAVA_URL,
            params={
                "after": int(mktime(start_of_week.timetuple())),
                "page": 1,
                "per_page": 50,
            },
            headers={
                "accept": "application/json",
                "authorization": "Bearer {}".format(self.access_token),
            },
        ).json()

        num_activities = len(response)
        distance_sum = 0.0
        time_sum = 0.0
        for activity in response:
            if activity["type"] == "Run":
                distance_sum += activity["distance"]
                time_sum += activity["moving_time"]

        self.canvas.SetImage(self.logo, 0, 0)
        graphics.DrawText(
            self.canvas,
            self.font,
            44,
            7,
            self.white,
            "W" + str(now.isocalendar()[1]),
        )

        self.canvas.SetImage(self.runner, 0, 9)
        graphics.DrawText(
            self.canvas,
            self.font,
            10,
            15,
            self.white,
            "{} run".format(num_activities) + ("s" if num_activities != 1 else ""),
        )

        self.canvas.SetImage(self.road, 0, 17)
        graphics.DrawText(
            self.canvas,
            self.font,
            10,
            23,
            self.white,
            "{:.1f} km".format(distance_sum / 1000),
        )

        self.canvas.SetImage(self.clock, 0, 25)
        graphics.DrawText(
            self.canvas,
            self.font,
            10,
            31,
            self.white,
            strftime("%-Hh %-Mm", gmtime(time_sum)),
        )

        self.sleep(15 * 1000 * 60)
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
            "EXPIRES_AT"
        ]
