import random
from dataclasses import dataclass, field
from typing import override

import pyray

from src.base import BaseApp


@dataclass(kw_only=True)
class P1BouncingCircle1(BaseApp):
    background_color = pyray.Color(0x18, 0x18, 0x18, 0xff)
    circle_color = pyray.Color(0xff, 0x18, 0x18, 0xff)

    r: float = field(init=False)
    min_r: float = field(init=False)
    max_r: float = field(init=False)
    pos_x: float = field(init=False)
    pos_y: float = field(init=False)
    speed_x: float = field(init=False)
    speed_y: float = field(init=False)
    speed_r: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.r: float = self.screen_width * 0.05
        self.min_r: float = self.r * 0.8
        self.max_r: float = self.r * 1.2
        self.pos_x: float = self.screen_width * 0.2
        self.pos_y: float = self.screen_height * 0.2
        self.speed_x: float = self.screen_width * 0.25
        self.speed_y: float = self.screen_height * 0.25
        self.speed_r: float = self.screen_width * 0.01

    @override
    def initialize(self):
        super().initialize()

    @override
    def update_state(self, dt):
        self.pos_x += dt * self.speed_x
        self.pos_y += dt * self.speed_y
        self.r += dt * self.speed_r
        if self.r > self.max_r:
            self.r = self.max_r
            self.speed_r *= -1
            self.speed_r *= random.uniform(0.9, 1.1)
        if self.r < self.min_r:
            self.r = self.min_r
            self.speed_r *= -1
            self.speed_r *= random.uniform(0.9, 1.1)
        if self.pos_x > self.screen_width - self.r:
            self.pos_x = self.screen_width - self.r
            self.speed_x *= -1
            self.speed_x *= random.uniform(0.9, 1.1)
        if self.pos_x < self.r:
            self.pos_x = self.r
            self.speed_x *= -1
            self.speed_x *= random.uniform(0.9, 1.1)
        if self.pos_y > self.screen_height - self.r:
            self.pos_y = self.screen_height - self.r
            self.speed_y *= -1
            self.speed_y *= random.uniform(0.9, 1.1)
        if self.pos_y < self.r:
            self.pos_y = self.r
            self.speed_y *= -1
            self.speed_y *= random.uniform(0.9, 1.1)

    @override
    def render_frame(self):
        pyray.clear_background(self.background_color)
        pyray.draw_circle(int(self.pos_x), int(self.pos_y), self.r, self.circle_color)


if __name__ == '__main__':
    rendering = False
    # rendering = True
    if not rendering:
        app = P1BouncingCircle1(screen_width=800,
                                screen_height=450,
                                window_title="P1BouncingCircle1",
                                )
    else:
        app = P1BouncingCircle1(screen_width=800,
                                screen_height=450,
                                window_title="P1BouncingCircle1",
                                fps=24,
                                rendering=True,
                                rendering_output_dir="output",
                                rendering_seconds=2.0,
                                )
    app.run()
