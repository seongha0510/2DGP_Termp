# game_over_state.py

from pico2d import *
import framework
import title_state  # 다시 타이틀로 돌아가기 위함
from constants import *

# 변수 선언
background = None
winner_frame = None  # 승리 배경 (winner.png)
winner_pose = None  # 승리 포즈 이미지
font_win = None  # 승리 메시지 폰트
font_info = None  # 안내 메시지 폰트

# play_state에서 받아올 정보들
winner_index = None  # 0: P1 승리, 1: P2 승리
p1_choice = 0  # P1이 선택한 캐릭터 번호
p2_choice = 1  # P2가 선택한 캐릭터 번호

# 캐릭터 번호별 승리 포즈 이미지 매핑
# (0번 캐릭터: 노란머리, 1번 캐릭터: 빨간머리)
WINNER_IMAGES = {
    0: 'winner_1p.png',  # 노란 머리 승리 포즈
    1: 'winner_2p.png'  # 빨간 머리 승리 포즈
}


def enter():
    global background, winner_frame, winner_pose, font_win, font_info
    global winner_index, p1_choice, p2_choice

    # 1. 게임 배경 (흐릿한 스테이지)
    background = load_image('Stage_blur.png')

    # 2. 승리 결과창 배경 (winner.png)
    winner_frame = load_image('winner.png')

    # 3. 승리 포즈 이미지 로드 (❗️ 핵심 수정 부분)
    # 단순히 winner_index를 쓰는 게 아니라, 승자가 "선택한 캐릭터 번호"를 확인해야 함
    winning_char_index = -1

    if winner_index == 0:  # P1 승리
        winning_char_index = p1_choice
    elif winner_index == 1:  # P2 승리
        winning_char_index = p2_choice

    # 해당 캐릭터의 승리 포즈 로드
    if winning_char_index in WINNER_IMAGES:
        winner_pose = load_image(WINNER_IMAGES[winning_char_index])
    else:
        winner_pose = None  # 무승부 등

    # 폰트 로드
    font_win = load_font('VITRO_CORE_TTF.ttf', 50)
    font_info = load_font('VITRO_CORE_TTF.ttf', 30)


def exit():
    global background, winner_frame, winner_pose, font_win, font_info
    del background
    del winner_frame
    del winner_pose
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

    # 2. 승리 프레임 (winner.png) 그리기
    frame_w, frame_h = 400, 500
    winner_frame.draw(center_x, center_y, frame_w, frame_h)

    # 3. 승리 캐릭터 포즈 그리기
    if winner_pose:
        pose_w, pose_h = 200, 350
        winner_pose.draw(center_x, center_y - 20, pose_w, pose_h)

        # 4. 텍스트 그리기
        win_text = f"PLAYER {winner_index + 1} WIN!!!"
        text_width = len(win_text) * 40

        # 프레임 상단부에 텍스트 배치
        font_win.draw(center_x - text_width // 2, center_y + 180, win_text, (255, 255, 0))  # 노란색

    else:
        # 무승부
        font_win.draw(center_x - 170, center_y, "DRAW GAME", (255, 255, 255))

    # 5. 안내 문구 (프레임 하단)
    font_info.draw(center_x - 150, center_y - 200, "PRESS ANY KEY", (0, 0, 0))

    update_canvas()