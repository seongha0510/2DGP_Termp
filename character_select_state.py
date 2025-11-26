# char_select_state.py

from pico2d import *
import framework
import play_state
from constants import *

# 변수 선언
background = None
frame1 = None  # 1P 빨간 테두리
frame2 = None  # 2P 초록 테두리
char1 = None  # 1P 캐릭터 이미지
char2 = None  # 2P 캐릭터 이미지
font = None


def enter():
    global background, frame1, frame2, char1, char2, font

    # 이미지 로드
    background = load_image('Stage_blur.png')
    frame1 = load_image('select1.png')
    frame2 = load_image('select2.png')
    char1 = load_image('selectcharacter1.png')
    char2 = load_image('selectcharacter2.png')

    # 안내 문구 폰트
    font = load_font('VITRO_CORE_TTF.ttf', 30)


def exit():
    global background, frame1, frame2, char1, char2, font
    del background
    del frame1
    del frame2
    del char1
    del char2
    del font


def handle_event(e):
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            framework.quit()
        elif e.key == SDLK_SPACE:
            # 스페이스바를 누르면 게임 시작!
            framework.change_state(play_state)


def update(dt):
    pass


def draw():
    clear_canvas()

    # 1. 배경 그리기
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    # --- 좌표 설정 ---
    # 화면 중앙(400)을 기준으로 좌우로 벌림
    p1_x = 250
    p2_x = 550
    center_y = 300

    # 박스 크기 (적당히 200x200 정도로 설정)
    box_size = 200

    # 2. 테두리 박스 그리기
    frame1.draw(p1_x, center_y, box_size, box_size)
    frame2.draw(p2_x, center_y, box_size, box_size)

    # 3. 캐릭터 그리기 (박스 안에 위치, 약간 작게)
    # 캐릭터 이미지가 박스보다 앞으로 튀어나오게 하려면 박스보다 나중에 그립니다.
    char_size = 180
    char1.draw(p1_x, center_y, char_size, char_size)
    char2.draw(p2_x, center_y, char_size, char_size)

    font.draw(p1_x - 15, center_y + 130, "1P", (255, 255, 255))
    font.draw(p2_x - 15, center_y + 130, "2P", (255, 255, 255))

    # 4. 안내 문구
    font.draw(CANVAS_W // 2 - 120, 100, "PRESS SPACE TO START", (255, 255, 255))

    update_canvas()