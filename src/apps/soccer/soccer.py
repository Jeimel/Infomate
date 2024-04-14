from api.base import Base
from rgbmatrix import RGBMatrix, graphics

from dataclasses import dataclass
from typing import List
from requests import get

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard"
FONT_NAME = "6x10"

# TODO: Add odds, different leagues


@dataclass
class Competitor:
    home: bool
    score: int
    name: str
    color: str
    logo: str


@dataclass
class Event:
    clock: str
    state: str
    competitors: List[Competitor]


@dataclass
class League:
    name: str
    events: List[Event]


class Soccer(Base):
    def __init__(self, matrix: RGBMatrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.font = Base.get_font(FONT_NAME)

    def run(self):
        league = Soccer.get_league()

        self.offscreen_canvas.Clear()
        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            15,
            15,
            self.textColor,
            league.events[0].competitors[0].name,
        )
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        self.msleep(10 * 1000)

    def get_league():
        response = get(url=ESPN_URL).json()
        league = League(response["leagues"][0]["name"], [])

        for event_json in response["events"]:
            league.events.append(Soccer.load_event(event_json))

        return league

    def load_event(event_json: dict) -> Event:
        event = Event(
            event_json["status"]["displayClock"],
            event_json["status"]["type"]["state"],
            [],
        )

        for competitor_json in event_json["competitions"][0]["competitors"]:
            event(Soccer.load_competitor(competitor_json))

        return event

    def load_competitor(competitor_json: dict) -> Competitor:
        return Competitor(
            competitor_json["homeAway"] == "home",
            int(competitor_json["score"]),
            competitor_json["team"]["shortDisplayName"],
            competitor_json["team"]["color"],
            competitor_json["team"]["logo"],
        )
