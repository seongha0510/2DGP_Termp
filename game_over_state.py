# game_over_state.py

from pico2d import *
import framework
import title_state
from constants import *

# 변수 선언
background = None
winner_frame = None
winner_pose = None
font_win = None
font_info = None
win_sound = None  # ❗️ 승리음 변수

winner_index = None
p1_choice = 0
p2_choice = 1

WINNER_IMAGES = {
    0: 'winner_1p.png',
    1: 'winner_2p.png'
}


def enter():
    global background, winner_frame, winner_pose, font_win, font_info
    global winner_index, p1_choice, p2_choice, win_sound

    # ❗️ 승리음 재생 (WAV로 로드)
    # 배경음악(bgm)은 framework에서 계속 재생 중입니다.
    win_sound = load_wav('Winner.mp3')
    win_sound.set_volume(64)
    win_sound.play()

    background = load_image('Stage_blur.png')
    winner_frame = load_image('winner.png')

    winning_char_index = -1
    if winner_index == 0:
        winning_char_index = p1_choice
    elif winner_index == 1:
        winning_char_index = p2_choice

    if winning_char_index in WINNER_IMAGES:
        winner_pose = load_image(WINNER_IMAGES[winning_char_index])
    else:
        winner_pose = None

    font_win = load_font('VITRO_CORE_TTF.ttf', 50)
    font_info = load_font('VITRO_CORE_TTF.ttf', 30)


def exit():
    global background, winner_frame, winner_pose, font_win, font_info, win_sound
    del background
    del winner_frame
    del winner_pose
    del font_win
    del font_info
    del win_sound  # ❗️


def handle_event(e):
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            framework.quit()
        else:
            framework.change_state(title_state)


def update(dt):
    pass


def draw():
    clear_canvas()

    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    center_x = CANVAS_W // 2
    center_y = CANVAS_H // 2

    frame_w, frame_h = 400, 500
    winner_frame.draw(center_x, center_y, frame_w, frame_h)

    if winner_pose:
        pose_w, pose_h = 200, 350
        winner_pose.draw(center_x, center_y - 20, pose_w, pose_h)

        win_text = f"PLAYER {winner_index + 1} WIN!!!"
        text_width = len(win_text) * 27

        font_win.draw(center_x - text_width // 2, center_y + 180, win_text, (255, 255, 0))

    else:
        font_win.draw(center_x - 170, center_y, "DRAW GAME", (255, 255, 255))

    font_info.draw(center_x - 130, center_y - 200, "PRESS ANY KEY", (0, 0, 0))

    update_canvas()