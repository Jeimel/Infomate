from api.base import Base
from rgbmatrix import RGBMatrix, graphics

from PIL import Image
from dataclasses import dataclass
from typing import List
from requests import get
from io import BytesIO

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard"
FONT_SMALL = "4x6"
FONT = "7x13B"

# TODO: Add odds, different leagues


@dataclass
class Competitor:
    home: bool
    score: str
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
        self.small_font = Base.get_font(FONT_SMALL)
        self.font = Base.get_font(FONT)
        self.index = 0

    def run(self):
        league = Soccer.get_league()
        if len(league.events) == 0:
            return False

        current_event = league.events[self.index]
        for i in range(len(league.events)):
            i = (i + self.index) % len(league.events)
            if league.events[i].state == "in":
                current_event = event
                break
        
        self.index = (self.index + 1) % len(league.events)

        self.offscreen_canvas.Clear()
        
        graphics.DrawText(
            self.offscreen_canvas,
            self.small_font,
            0,
            32,
            graphics.Color(255, 255, 255),
            league.name.upper(),
        )
        graphics.DrawText(
            self.offscreen_canvas,
            self.small_font,
            65 - len(current_event.clock) * 4,
            32,
            graphics.Color(255, 255, 255),
            current_event.clock
        )
        
        for competitor in current_event.competitors:
            color = Soccer.hex_to_rgb(competitor.color)
            
            y_range = range(0, 13) if competitor.home else range(13, 26)
            for y in y_range:
                for x in range(0, 64):
                    self.offscreen_canvas.SetPixel(x, y, color[0], color[1], color[2]);
            
            logo_transparent = Image.open(BytesIO(get(competitor.logo).content)).resize((13, 13))
            logo = Image.new("RGBA", logo_transparent.size, color)
            logo.paste(logo_transparent, mask=logo_transparent)

            image_y = 0 if competitor.home else 13
            self.offscreen_canvas.SetImage(logo.convert("RGB"), 0, image_y)

            text_y = 11 if competitor.home else 24
            graphics.DrawText(
                self.offscreen_canvas,
                self.font,
                18,
                text_y,
                graphics.Color(255, 255, 255),
                competitor.name
            )
            graphics.DrawText(
                self.offscreen_canvas,
                self.font,
                54,
                text_y,
                graphics.Color(255, 255, 255),
                competitor.score
            )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        self.msleep(15 * 1000)
        return True

    def get_league():
        response = get(url=ESPN_URL).json()
        league = League(response["leagues"][0]["abbreviation"], [])

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
            event.competitors.append(Soccer.load_competitor(competitor_json))

        return event

    def load_competitor(competitor_json: dict) -> Competitor:
        return Competitor(
            competitor_json["homeAway"] == "home",
            competitor_json["score"],
            competitor_json["team"]["abbreviation"],
            competitor_json["team"]["color"],
            competitor_json["team"]["logo"].replace("https://a.espncdn.com/", "https://a.espncdn.com/combiner/i?img=") + "&h=50&w=50",
        )

    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
