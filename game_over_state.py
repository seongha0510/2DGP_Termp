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

# play_state에서 받아올 승자 정보 (None이면 무승부, 0이면 P1, 1이면 P2)
winner_index = None

# 캐릭터별 승리 포즈 이미지 경로 (0: 노란머리, 1: 빨간머리)
# (주의: 캐릭터 선택에 따라 이미지가 달라져야 한다면 로직이 더 필요하지만,
# 일단 보내주신 파일명대로 winner_1p, winner_2p를 매핑합니다.)
WINNER_IMAGES = {
    0: 'winner_1p.png',  # P1 승리 시 보여줄 이미지
    1: 'winner_2p.png'  # P2 승리 시 보여줄 이미지
}


def enter():
    global background, winner_frame, winner_pose, font_win, font_info, winner_index

    # 1. 게임 배경 (흐릿한 스테이지)
    background = load_image('Stage_blur.png')

    # 2. 승리 결과창 배경 (winner.png)
    winner_frame = load_image('winner.png')

    # 3. 승리 포즈 이미지 로드
    if winner_index in WINNER_IMAGES:
        winner_pose = load_image(WINNER_IMAGES[winner_index])
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
    # 크기 조절 (예: 400x500 정도)
    frame_w, frame_h = 400, 500
    winner_frame.draw(center_x, center_y, frame_w, frame_h)

    # 3. 승리 캐릭터 포즈 그리기
    if winner_pose:
        # 프레임 중앙에 배치 (크기는 적당히 조절, 예: 250x350)
        # 비율 유지하고 싶으면 원본 비율 계산 필요하지만 일단 강제 크기 지정
        pose_w, pose_h = 200, 350
        # 포즈를 프레임 중앙보다 살짝 아래에 배치
        winner_pose.draw(center_x, center_y - 20, pose_w, pose_h)

        # 4. 텍스트 그리기
        win_text = f"PLAYER {winner_index + 1} WIN!!!"
        text_width = len(win_text) * 28

        # 프레임 상단부에 텍스트 배치
        font_win.draw(center_x - text_width // 2, center_y + 180, win_text, (255, 255, 0))  # 노란색

    else:
        # 무승부
        font_win.draw(center_x - 150, center_y, "DRAW GAME", (255, 255, 255))

    # 5. 안내 문구 (프레임 하단)
    font_info.draw(center_x - 130, center_y - 200, "PRESS ANY KEY", (0, 0, 0))  # 검은색 (흰 배경 위니까)

    update_canvas()