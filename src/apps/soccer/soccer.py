from api.base import Base
from rgbmatrix import FrameCanvas, graphics

from datetime import datetime
from PIL import Image
from dataclasses import dataclass
from typing import List
from requests import get
from io import BytesIO
from os import getenv


DATE_FORMAT = "%Y-%m-%dT%H:%MZ"
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard"
FONT_SMALL_NAME = "4x6"
FONT_NAME = "7x13B"
DEFAULT_LEAGUE = "Bundesliga"
LEAGUES = {
    "Bundesliga": {"code": "ger.1", "abbreviation": "Bund"},
    "La Liga": {"code": "esp.1", "abbreviation": "Liga"},
    "Premier League": {"code": "eng.1", "abbreviation": "PL"},
    "Champions League": {"code": "uefa.champions", "abbreviation": "UCL"},
    "Europa League": {"code": "uefa.europa", "abbreviation": "Euro"},
    "Ligue 1": {"code": "fra.1", "abbreviation": "L1"},
    "Serie A": {"code": "ita.1", "abbreviation": "SerA"},
}


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
        self.league_name = LEAGUES.get(
            getenv("SOCCER_LEAGUE", DEFAULT_LEAGUE), LEAGUES[DEFAULT_LEAGUE]
        )

        self.small_font = Base.get_font(FONT_SMALL_NAME)
        self.font = Base.get_font(FONT_NAME)
        self.white = graphics.Color(255, 255, 255)
        self.index = 0

    def run(self) -> bool:
        league = Soccer.get_league(
            self.league_name["code"], self.league_name["abbreviation"]
        )
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
            start, end = (0, 13) if competitor.home else (13, 26)
            self.draw_rect(self.canvas, 0, start, 64, end, competitor.color)
            self.draw_competitor(competitor, range(start, end))

        self.sleep(15 * 1000)
        return True

    def draw_competitor(self, competitor: Competitor, y_range: range):
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

    @staticmethod
    def env() -> bool:
        return True

    @staticmethod
    def variables() -> list:
        return ["LEAGUE"]

    @staticmethod
    def get_league(
        code: str,
        abbreviation: str,
    ):
        response = get(url=ESPN_URL.format(league=code)).json()
        league = League(abbreviation, [])

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
