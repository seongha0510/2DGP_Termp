# title_state.py

from pico2d import *
import framework
import play_state
from constants import *  # ❗️ [추가] 상수를 사용하기 위해 꼭 필요합니다!

image = None
font = None


def enter():
    global image, font
    # 파일명이 정확한지 확인해주세요 (main.png 또는 main.jpg)
    image = load_image('main.png')
    font = load_font('VITRO_CORE_TTF.ttf', 30)


def exit():
    global image, font
    del image
    del font


def handle_event(e):
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            framework.quit()
        else:
            # 아무 키나 누르면 게임 화면으로 넘어감
            framework.change_state(play_state)


def update(dt):
    pass


def draw():
    clear_canvas()
    # 이제 constants.py를 임포트했으므로 CANVAS_W, CANVAS_H를 알 수 있습니다.
    image.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    text = "[PRESS ANY BUTTON !]"

    # 폰트 너비/높이 계산이 안 될 경우를 대비해 try-except나 고정값 사용 가능하지만,
    # 일단 기본 로직대로 진행합니다.
    text_x = CANVAS_W // 2 - 150  # 대략적인 중앙 정렬
    text_y = 100  # 화면 하단부

    font.draw(text_x, text_y, text, (255, 255, 255))

    update_canvas()