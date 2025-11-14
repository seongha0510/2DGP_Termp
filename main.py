# main.py

import framework  # 만들어둔 프레임워크를 불러옴
import sys  # <--- ❗️ 1. sys 임포트 (필수)
from pico2d import *
from character import Character  # 만들어둔 캐릭터 클래스를 불러옴
from constants import *  # 만들어둔 상수를 모두 불러옴

# main.py에서만 사용할 변수
background = None
p1 = None
p2 = None
running = True  # 게임 루프 실행 여부


# --- ❗️ 2. 충돌 검사 함수 (새로 추가) ---
def check_collision(a, b):
    """a와 b의 히트박스를 가져와 충돌 여부를 True/False로 반환합니다."""
    left_a, bottom_a, right_a, top_a = a.get_hitbox()
    left_b, bottom_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True  # 겹침


# --- framework.py가 호출할 함수들 ---

def enter():
    """게임을 시작할 때 딱 한 번 실행됩니다."""
    global background, p1, p2

    background = load_image('Stage.png')

    # --- P1 애셋, 프레임, 키, 룰 정의 ---
    p1_assets = {
        'stand': load_image('character1.png'),
        'jump': load_image('character1_jump.png'),
        'divekick': load_image('character1_divekick.png'),
        'walk': load_image('character1_walk.png')
    }
    p1_frames = {
        'jump_rise': P1_JUMP_RISE,
        'jump_fall': P1_JUMP_FALL,
        'walk': P1_WALK_FRAMES,
        'walk_fps': P1_WALK_FPS
    }
    p1_keys = {
        'left': SDLK_a, 'right': SDLK_d, 'up': SDLK_w, 'down': SDLK_s
    }
    p1_rules = {
        'padding': P1_WALK_PADDING,
        'dive_speed': 700.0,
        'dive_scale': 1.0,
        'jump_flip': False
    }

    # --- P2 애셋, 프레임, 키, 룰 정의 ---
    p2_assets = {
        'stand': load_image('character_2.png'),
        'jump': load_image('character2_jump.png'),
        'divekick': load_image('character2_divekick.png'),
        'walk': load_image('character_2_walk.png')
    }
    p2_frames = {
        'jump_rise': P2_JUMP_RISE,
        'jump_fall': P2_JUMP_FALL,
        'walk': P2_WALK_FRAMES,
        'walk_fps': P2_WALK_FPS
    }
    p2_keys = {
        'left': SDLK_LEFT, 'right': SDLK_RIGHT, 'up': SDLK_UP, 'down': SDLK_DOWN
    }
    p2_rules = {
        'padding': P2_WALK_PADDING,
        'dive_speed': 700.0,
        'dive_scale': 1.15,
        'jump_flip': True
    }

    # --- 캐릭터 객체 생성 ---
    p1 = Character(
        x=p1_assets['stand'].w * 2 // 2,
        direction=1,
        keys=p1_keys,
        assets=p1_assets,
        frames=p1_frames,
        rules=p1_rules
    )
    p2 = Character(
        x=CANVAS_W - p2_assets['stand'].w * 2 // 2,
        direction=-1,
        keys=p2_keys,
        assets=p2_assets,
        frames=p2_frames,
        rules=p2_rules
    )


def exit():
    """게임을 종료할 때 딱 한 번 실행됩니다."""
    global background, p1, p2
    del background
    del p1
    del p2


def handle_event(e):
    """키보드 입력 등을 처리합니다."""
    global running
    if e.type == SDL_QUIT:
        running = False
    elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        running = False
    else:
        # 각 캐릭터가 스스로 이벤트를 처리하도록 명령
        p1.handle_event(e)
        p2.handle_event(e)


def update(dt):
    """모든 게임 객체의 상태를 업데이트합니다."""
    p1.update(dt)
    p2.update(dt)

    # --- ❗️ 3. 충돌 검사 및 데미지 처리 (새로 추가) ---
    if check_collision(p1, p2):
        # P1이 다이브킥 중이고 P2와 부딪혔다면
        if p1.is_dive_kicking:
            p2.take_damage(1)  # P2 데미지
            print(f"P1 HITS! P2 HP: {p2.hp}")  # 콘솔에 HP 출력

        # P2가 다이브킥 중이고 P1과 부딪혔다면
        if p2.is_dive_kicking:
            p1.take_damage(1)  # P1 데미지
            print(f"P2 HITS! P1 HP: {p1.hp}")  # 콘솔에 HP 출력


def draw():
    """모든 게임 객체를 화면에 그립니다."""
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)
    p1.draw()
    p2.draw()

    # --- ❗️ 4. (디버깅용) 히트박스 그리기 (새로 추가, 주석 처리) ---
    # (l, b, r, t) = p1.get_hitbox()
    # draw_rectangle(l, b, r, t)
    # (l, b, r, t) = p2.get_hitbox()
    # draw_rectangle(l, b, r, t)

    update_canvas()


# --- 이 파일이 메인 파일로 실행될 때 ---
if __name__ == '__main__':
    framework.run(sys.modules[__name__])