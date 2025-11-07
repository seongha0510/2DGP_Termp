from pico2d import *

open_canvas(800, 600)

andy_sheet = load_image('Andy.png')
background = load_image('Stage.png')

sprite_left = 5
sprite_bottom = 3307
sprite_width = 75
sprite_height = 115

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

running = True
while running:
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    clear_canvas()

    # 배경 이미지를 캔버스에 맞게 비율을 유지하면서 채웁니다(가운데 정렬, 잘림 발생 가능).
    try:
        bg_w = background.w
        bg_h = background.h
    except Exception:
        try:
            bg_w = background.get_width()
            bg_h = background.get_height()
        except Exception:
            bg_w, bg_h = CANVAS_W, CANVAS_H

    scale = max(CANVAS_W / bg_w, CANVAS_H / bg_h)
    draw_w = int(bg_w * scale)
    draw_h = int(bg_h * scale)
    # 중앙(400,300)에 스케일된 크기로 그리면 캔버스를 완전히 덮습니다.
    background.draw(CANVAS_W // 2, CANVAS_H // 2, draw_w, draw_h)

    andy_sheet.clip_draw(sprite_left, sprite_bottom, sprite_width, sprite_height, CANVAS_W // 2, CANVAS_H // 2)
    update_canvas()
    delay(1/60)

close_canvas()