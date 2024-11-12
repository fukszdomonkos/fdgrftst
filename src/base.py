import datetime
import pathlib
import random
import subprocess
from dataclasses import dataclass, field
from typing import Optional

import ffmpeg
import pyray
from raylib import ffi


@dataclass(kw_only=True)
class BaseApp:
    screen_width: int
    screen_height: int
    window_title: str
    fps: int=60
    random_seed: int    = 186484546135
    rendering: bool= False
    rendering_output_dir: str= "output"
    rendering_seconds: float= 10.0

    running: bool = False
    state: dict = field(default_factory=dict)
    rendering_ffmpeg_process: Optional[subprocess.Popen] = None

    # def __init__(self, width, height, title,
    #              fps=60,
    #              random_seed=186484546135,
    #              rendering=False,
    #              rendering_output_dir="output",
    #              rendering_seconds=10.0
    #              ):
    #     self.screen_width = width
    #     self.screen_height = height
    #     self.window_title = title
    #     self.fps = fps
    #     self.random_seed = random_seed
    #     self.rendering = rendering
    #     self.rendering_output_dir = rendering_output_dir
    #     self.rendering_seconds = rendering_seconds

    def __post_init__(self):
        # To be overridden by subclasses as needed
        pass

    def initialize(self):
        random.seed(self.random_seed)
        pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_ERROR)
        pyray.init_window(self.screen_width, self.screen_height, self.window_title)
        pyray.set_target_fps(self.fps)
        if self.rendering:
            self.initialize_ffmpeg()

    def initialize_ffmpeg(self):
        pathlib.Path(self.rendering_output_dir).mkdir(parents=True, exist_ok=True)
        self.rendering_ffmpeg_process = (ffmpeg
                                         .input('pipe:', loglevel='verbose', format='rawvideo', pix_fmt='rgba',
                                                s=f'{self.screen_width}x{self.screen_height}', r=self.fps
                                                )
                                         .output(f'{self.rendering_output_dir}/'
                                                 f'render-'
                                                 f'{self.window_title}-'
                                                 f'{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'
                                                 f'.mp4')
                                         .overwrite_output()
                                         .run_async(pipe_stdin=True))

    def terminate(self):
        pyray.close_window()
        if self.rendering:
            self.terminate_ffmpeg()

    def terminate_ffmpeg(self):
        self.rendering_ffmpeg_process.stdin.close()

    def handle_input(self):
        # To be overridden by subclasses as needed
        pass

    def update_state(self, delta_time):
        # To be overridden by subclasses as needed
        pass

    def render_frame(self):
        # To be overridden by subclasses
        pass

    def run(self):
        self.initialize()
        self.running = True
        current_frame_count = 0
        while self.running and not pyray.window_should_close():
            current_frame_count += 1
            if self.rendering:
                delta_time = 1 / self.fps
                if current_frame_count > self.fps * self.rendering_seconds:
                    self.stop()
            else:
                delta_time = pyray.get_frame_time()

            # Core loop functions
            if not self.rendering:
                self.handle_input()
            self.update_state(delta_time)

            # Render phase
            pyray.begin_drawing()

            render_texture = None
            if self.rendering:
                render_texture = pyray.load_render_texture(self.screen_width, self.screen_height)
                pyray.begin_texture_mode(render_texture)

            self.render_frame()

            if self.rendering:
                pyray.end_texture_mode()
                image = pyray.load_image_from_texture(render_texture.texture)
                image_data = ffi.buffer(image.data, self.screen_width * self.screen_height * 4)[:]
                # flip image by rows
                image_data = b''.join([image_data[i:i + self.screen_width * 4] for i in range(0, len(image_data), self.screen_width * 4)][::-1])
                self.rendering_ffmpeg_process.stdin.write(image_data)
                del image_data
                pyray.unload_image(image)
                pyray.unload_render_texture(render_texture)
            pyray.end_drawing()

        self.terminate()

    def stop(self):
        self.running = False
