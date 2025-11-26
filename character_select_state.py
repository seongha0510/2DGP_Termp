# char_select_state.py

from pico2d import *
import framework
import play_state
from constants import *

# 변수 선언
background = None
frame1 = None  # 1P 테두리
frame2 = None  # 2P 테두리
char_images = []  # 캐릭터 이미지들을 담을 리스트
font = None

# 선택된 캐릭터 번호 (0: 캐릭터1, 1: 캐릭터2)
p1_select = 0
p2_select = 1


def enter():
    global background, frame1, frame2, char_images, font, p1_select, p2_select

    # 이미지 로드
    background = load_image('Stage_blur.png')
    frame1 = load_image('select1.png')
    frame2 = load_image('select2.png')

    # 캐릭터 이미지를 리스트에 순서대로 담습니다.
    char_images = []
    char_images.append(load_image('selectcharacter1.png'))  # 인덱스 0: 노란 머리
    char_images.append(load_image('selectcharacter2.png'))  # 인덱스 1: 빨간 머리

    font = load_font('VITRO_CORE_TTF.ttf', 30)

    # 초기 선택 (1P는 0번, 2P는 1번 캐릭터)
    p1_select = 0
    p2_select = 1


def exit():
    global background, frame1, frame2, char_images, font
    del background
    del frame1
    del frame2
    # 리스트 내의 이미지들도 삭제
    for img in char_images:
        del img
    del char_images
    del font


def handle_event(e):
    global p1_select, p2_select

    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            framework.quit()

        # --- 1P 선택 로직 (A, D) ---
        elif e.key == SDLK_a:
            p1_select = (p1_select - 1) % len(char_images)
        elif e.key == SDLK_d:
            p1_select = (p1_select + 1) % len(char_images)

        # --- 2P 선택 로직 (좌, 우) ---
        elif e.key == SDLK_LEFT:
            p2_select = (p2_select - 1) % len(char_images)
        elif e.key == SDLK_RIGHT:
            p2_select = (p2_select + 1) % len(char_images)

        # --- 게임 시작 (스페이스바) ---
        elif e.key == SDLK_SPACE:
            # 선택한 캐릭터 정보를 play_state로 전달
            play_state.p1_choice = p1_select
            play_state.p2_choice = p2_select

            # 게임 화면으로 전환
            framework.change_state(play_state)


def update(dt):
    pass


def draw():
    clear_canvas()

    # 1. 배경
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    # 좌표 및 크기 설정
    p1_x = 250
    p2_x = 550
    center_y = 300
    box_size = 200
    char_size = 180

    # 2. 테두리 박스
    frame1.draw(p1_x, center_y, box_size, box_size)
    frame2.draw(p2_x, center_y, box_size, box_size)

    # 3. 캐릭터 그리기 (좌우 반전 로직 적용)

    # [1P] 왼쪽 위치
    if p1_select == 0:
        # 0번(노랑): 그대로
        char_images[0].draw(p1_x, center_y, char_size, char_size)
    else:
        # 1번(빨강): 뒤집기('h')
        char_images[1].composite_draw(0, 'h', p1_x, center_y, char_size, char_size)

    # [2P] 오른쪽 위치
    if p2_select == 0:
        # 0번(노랑): 뒤집기('h')
        char_images[0].composite_draw(0, 'h', p2_x, center_y, char_size, char_size)
    else:
        # 1번(빨강): 그대로
        char_images[1].draw(p2_x, center_y, char_size, char_size)

    # 4. 텍스트 표시
    # "1P", "2P" 라벨
    font.draw(p1_x - 20, center_y + 130, "1P", (255, 255, 255))
    font.draw(p2_x - 20, center_y + 130, "2P", (255, 255, 255))

    # 조작 설명
    info_text = "1P [ A / D ]    SELECT    [ ◀ / ▶ ] 2P"
    font.draw(CANVAS_W // 2 - 290, 100, info_text, (255, 255, 255))

    # 시작 문구
    start_text = "- PRESS SPACE TO START -"
    font.draw(CANVAS_W // 2 - 190, 60, start_text, (255, 255, 0))

    update_canvas()