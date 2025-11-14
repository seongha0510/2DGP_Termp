# framework.py

from pico2d import *
import time

# dt 계산을 위한 시간 변수
_last_time = 0.0
_frame_time = 0.0


def run(main_state):
    global _last_time, _frame_time

    # 1. 초기화
    open_canvas(main_state.CANVAS_W, main_state.CANVAS_H)
    main_state.enter()

    _last_time = time.time()

    # 2. 메인 루프
    while main_state.running:
        # 2-1. 시간 계산 (dt)
        now = time.time()
        _frame_time = now - _last_time
        _last_time = now

        # 2-2. 입력 처리
        events = get_events()
        for e in events:
            main_state.handle_event(e)

        # 2-3. 상태 업데이트
        main_state.update(_frame_time)

        # 2-4. 그리기
        clear_canvas()
        main_state.draw()
        update_canvas()

        delay(0.01)  # CPU 부담 감소

    # 3. 종료
    main_state.exit()
    close_canvas()