from api.base import Base
from rgbmatrix import FrameCanvas, graphics

from datetime import datetime
from PIL import Image
from dataclasses import dataclass
from typing import List
from requests import get
from io import BytesIO

DATE_FORMAT = "%Y-%m-%dT%H:%MZ"
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard"
FONT_SMALL_NAME = "4x6"
FONT_NAME = "7x13B"
LEAGUE_ABBREVIATION = {"GER.1": "Bund"}


@dataclass
class Competitor:
    home: bool
    score: str
    name: str
    color: tuple[int, int, int]
    text_color: graphics.Color
    logo: str


@dataclass
class Event:
    clock: str
    state: str
    date: datetime
    competitors: List[Competitor]


@dataclass
class League:
    name: str
    events: List[Event]


class Soccer(Base):

    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)
        self.small_font = Base.get_font(FONT_SMALL_NAME)
        self.font = Base.get_font(FONT_NAME)
        self.white = graphics.Color(255, 255, 255)
        self.index = 0

    def run(self) -> bool:
        league = Soccer.get_league()
        if len(league.events) == 0:
            return False

        current_event = league.events[self.index]
        for i in range(len(league.events)):
            i = (i + self.index) % len(league.events)
            if league.events[i].state == "in":
                current_event = league.events[i]
                break

        self.index = (self.index + 1) % len(league.events)

        graphics.DrawText(
            self.canvas,
            self.small_font,
            0,
            32,
            self.white,
            league.name.upper(),
        )

        time = (
            "OVER"
            if current_event.state == "post"
            else (
                current_event.date.strftime("%a %H:%M")
                if current_event.state == "pre"
                else current_event.clock
            )
        )
        graphics.DrawText(
            self.canvas,
            self.small_font,
            65 - len(time) * 4,
            32,
            self.white,
            time,
        )

        for competitor in current_event.competitors:
            y_range = range(0, 13) if competitor.home else range(13, 26)
            for y in y_range:
                for x in range(0, 64):
                    self.canvas.SetPixel(
                        x,
                        y,
                        competitor.color[0],
                        competitor.color[1],
                        competitor.color[2],
                    )

            logo_transparent = Image.open(BytesIO(get(competitor.logo).content))
            logo = Image.new("RGBA", logo_transparent.size, competitor.color)
            logo.paste(logo_transparent, mask=logo_transparent)

            image_y = 0 if competitor.home else 13
            self.canvas.SetImage(logo.convert("RGB").resize((13, 13)), 0, image_y)

            text_y = 11 if competitor.home else 24
            graphics.DrawText(
                self.canvas,
                self.font,
                18,
                text_y,
                competitor.text_color,
                competitor.name,
            )
            graphics.DrawText(
                self.canvas,
                self.font,
                54,
                text_y,
                competitor.text_color,
                competitor.score,
            )

        self.sleep(15 * 1000)
        return True

    @staticmethod
    def get_league():
        response = get(url=ESPN_URL).json()
        name = response["leagues"][0]["midsizeName"]
        if name in LEAGUE_ABBREVIATION:
            name = LEAGUE_ABBREVIATION[name]
        league = League(name, [])

        for event_json in response["events"]:
            league.events.append(Soccer.load_event(event_json))

        return league

    @staticmethod
    def load_event(event_json: dict) -> Event:
        event = Event(
            event_json["status"]["displayClock"],
            event_json["status"]["type"]["state"],
            datetime.strptime(event_json["date"], DATE_FORMAT),
            [],
        )

        for competitor_json in event_json["competitions"][0]["competitors"]:
            event.competitors.append(Soccer.load_competitor(competitor_json))

        return event

    @staticmethod
    def load_competitor(competitor_json: dict) -> Competitor:
        color = Soccer.hex_to_rgb(competitor_json["team"]["color"])
        text_color = Soccer.hex_to_rgb(competitor_json["team"]["alternateColor"])

        return Competitor(
            competitor_json["homeAway"] == "home",
            competitor_json["score"],
            competitor_json["team"]["abbreviation"],
            (color[0], color[1], color[2]),
            graphics.Color(text_color[0], text_color[1], text_color[2]),
            competitor_json["team"]["logo"].replace(
                "https://a.espncdn.com/", "https://a.espncdn.com/combiner/i?img="
            )
            + "&h=50&w=50",
        )

    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
