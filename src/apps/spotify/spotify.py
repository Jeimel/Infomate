from api.base import Base
from rgbmatrix import FrameCanvas

from argparse import ArgumentParser


class Spotify(Base):
    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)

        self.parser = ArgumentParser()
        self.parser.add_argument(
            "--client-id",
            action="store",
            help="The Client ID generated after registering your application.",
            type=str,
        )
        self.parser.add_argument(
            "--client-secret",
            action="store",
            help="The Client secret generated after registering your application.",
            type=str,
        )

        self.args = self.parser.parse_args()
