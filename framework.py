# framework.py (수정된 버전 - open_canvas 추가)

from pico2d import *
import time

running = True
stack = None


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
    global running, stack

    # ❗️ [수정] 게임 시작 전에 반드시 캔버스(창)를 먼저 열어야 합니다!
    open_canvas(800, 600)  # 너비 800, 높이 600으로 창 열기

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

    close_canvas()