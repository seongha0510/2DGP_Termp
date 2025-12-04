# game_over_state.py

from pico2d import *
import framework
import title_state  # 다시 타이틀로 돌아가기 위함
from constants import *

# 변수 선언
background = None
winner_image = None  # 승리한 캐릭터 이미지
font_win = None  # 승리 메시지 폰트 (큰 글씨)
font_info = None  # 안내 메시지 폰트 (작은 글씨)

# play_state에서 받아올 승자 정보 (None이면 무승부, 0이면 P1, 1이면 P2)
winner_index = None


def enter():
    global background, winner_image, font_win, font_info, winner_index

    # 배경 이미지 로드
    background = load_image('Stage_blur.png')

    # 승리한 캐릭터 이미지 로드 (play_state에서 winner_index를 받아옴)
    if winner_index == 0:  # P1 승리 (노란 머리)
        winner_image = load_image('character1.png')
    elif winner_index == 1:  # P2 승리 (빨간 머리)
        winner_image = load_image('character_2.png')
    else:
        # 무승부일 경우 (일단 이미지 없음)
        winner_image = None

    # 폰트 로드
    font_win = load_font('VITRO_CORE_TTF.ttf', 60)  # 큰 폰트
    font_info = load_font('VITRO_CORE_TTF.ttf', 30)  # 작은 폰트


def exit():
    global background, winner_image, font_win, font_info
    del background
    del winner_image
    del font_win
    del font_info


def handle_event(e):
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            framework.quit()
        else:
            # 아무 키나 누르면 타이틀 화면으로 돌아감
            framework.change_state(title_state)


def update(dt):
    pass


def draw():
    clear_canvas()

    # 1. 배경 그리기
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    center_x = CANVAS_W // 2
    center_y = CANVAS_H // 2

    # 2. 승리 캐릭터 및 텍스트 그리기
    if winner_index is not None:
        # 승리 캐릭터를 중앙에 크게 그리기 (크기 300x300)
        winner_image.draw(center_x, center_y, 300, 300)

        # 승리 텍스트 설정
        win_text = f"PLAYER {winner_index + 1} WIN!!!"

        # 텍스트 너비 계산 (중앙 정렬용)
        # get_width가 없는 경우 대략적인 너비를 계산해서 사용
        text_width = len(win_text) * 30

        # 캐릭터 머리 위에 승리 텍스트 그리기 (노란색 강조)
        font_win.draw(center_x - text_width // 2, center_y + 200, win_text, (255, 255, 0))

    else:
        # 무승부 텍스트
        font_win.draw(center_x - 150, center_y + 50, "DRAW GAME", (255, 255, 255))

    # 3. 안내 문구 그리기 (하단)
    font_info.draw(center_x - 180, 100, "- PRESS ANY KEY -", (255, 255, 255))

    update_canvas()