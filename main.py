import pathlib
import random

import ffmpeg
from pyray import *
from raylib import ffi

# rendering_mode = False
rendering_mode = True

random_seed = 186484546135

# screen_width = 1280
# screen_height = 720
# screen_width = 1920
# screen_height = 1080
screen_width = 3840
screen_height = 2160

frame_rate = 60
# frame_rate = 20

render_second = 60
# render_second = 4

background_color = Color(0x18, 0x18, 0x18, 0xff)
circle_color = Color(0xff, 0x18, 0x18, 0xff)
# r: float = 50
r: float = screen_width * 0.05
min_r: float = r*0.8
max_r: float = r*1.2
# pos_x: float = 300
# pos_y: float = 300
pos_x: float = screen_width*0.2
pos_y: float = screen_height*0.2
# speed_x: float = 300
# speed_y: float = 300
# speed_r: float = 20
speed_x: float = screen_width*0.25
speed_y: float = screen_height*0.25
speed_r: float = screen_width*0.01


def main():
    init_window(screen_width, screen_height, "Raylib")
    set_target_fps(frame_rate)
    random.seed(random_seed)

    if not rendering_mode:
        while not window_should_close():
            begin_drawing()

            dt = get_frame_time()
            render_frame(dt)

            end_drawing()
    else:
        pathlib.Path("output").mkdir(parents=True, exist_ok=True)
        ff = (ffmpeg
              .input('pipe:', loglevel='verbose', format='rawvideo', pix_fmt='rgba', s=f'{screen_width}x{screen_height}', r=frame_rate)
              .output('output/output.mp4')
              .overwrite_output()
              .run_async(pipe_stdin=True))
        for i in range(frame_rate * render_second):
            if window_should_close():
                break
            begin_drawing()

            render_texture = load_render_texture(screen_width, screen_height)
            begin_texture_mode(render_texture)

            dt = 1 / frame_rate
            render_frame(dt)

            end_texture_mode()
            if False:
                draw_texture(render_texture.texture, 0, 0, WHITE)
            image = load_image_from_texture(render_texture.texture)
            data = ffi.buffer(image.data, screen_width * screen_height * 4)[:]
            #flip image by rows
            data = b''.join([data[i:i + screen_width * 4] for i in range(0, len(data), screen_width * 4)][::-1])
            ff.stdin.write(data)

            end_drawing()
        ff.stdin.close()
    close_window()


def render_frame(dt: float):
    global r, pos_x, pos_y, speed_x, speed_y, speed_r
    pos_x += dt * speed_x
    pos_y += dt * speed_y
    r += dt * speed_r
    if r > max_r:
        r = max_r
        speed_r *= -1
        speed_r *= random.uniform(0.9, 1.1)
    if r < min_r:
        r = min_r
        speed_r *= -1
        speed_r *= random.uniform(0.9, 1.1)
    if pos_x > screen_width - r:
        pos_x = screen_width - r
        speed_x *= -1
        speed_x *= random.uniform(0.9, 1.1)
    if pos_x < r:
        pos_x = r
        speed_x *= -1
        speed_x *= random.uniform(0.9, 1.1)
    if pos_y > screen_height - r:
        pos_y = screen_height - r
        speed_y *= -1
        speed_y *= random.uniform(0.9, 1.1)
    if pos_y < r:
        pos_y = r
        speed_y *= -1
        speed_y *= random.uniform(0.9, 1.1)
    clear_background(background_color)
    draw_circle(int(pos_x), int(pos_y), r, circle_color)


if __name__ == '__main__':
    main()
