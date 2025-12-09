# framework.py

from pico2d import *
import time

running = True
stack = None
bgm = None  # ❗️ 전역 BGM 변수


def change_state(state_module):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    stack.append(state_module)
    state_module.enter()


def quit():
    global running
    running = False


def run(start_state_module):
    global running, stack, bgm

    # 1. 초기화 (반드시 캔버스 먼저 열기)
    open_canvas(800, 600)

    # --- ❗️ [추가] BGM 로드 및 재생 ---
    # 여기서 한 번만 로드해서 게임 내내 씁니다.
    bgm = load_music('bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    # --------------------------------

    running = True
    stack = [start_state_module]
    start_state_module.enter()

    current_time = time.time()

    while running:
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time

        events = get_events()
        for e in events:
            stack[-1].handle_event(e)

        stack[-1].update(frame_time)

        clear_canvas()
        stack[-1].draw()
        update_canvas()

        delay(0.01)

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()

    # 종료 시 BGM 정리
    del bgm
    close_canvas()