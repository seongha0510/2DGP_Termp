# main.py

import framework
import sys
from pico2d import *
from character import Character
from constants import *
from hp_bar import HpBar  # (이 부분은 기존과 동일)

# main.py에서만 사용할 변수
background = None
p1 = None
p2 = None
hp_bar = None  # --- ❗️ 1. [수정] P1, P2 HP 바 변수를 하나로 통합 ---
running = True


def check_collision(a, b):
    left_a, bottom_a, right_a, top_a = a.get_hitbox()
    left_b, bottom_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


# --- framework.py가 호출할 함수들 ---

def enter():
    global background, p1, p2, hp_bar  # --- ❗️ 2. [수정] global 변수 ---

    background = load_image('Stage.png')

    # --- P1 애셋, 프레임, 키, 룰 정의 (기존과 동일) ---
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

    # --- P2 애셋, 프레임, 키, 룰 정의 (기존과 동일) ---
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

    # --- 캐릭터 객체 생성 (기존과 동일) ---
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

    # --- ❗️ 3. [수정] HP 바 객체 생성 ---
    # 통합 HP 바의 크기 및 위치 (화면 중앙 상단)
    BAR_W, BAR_H = 600, 50  # 너비를 600 정도로 크게 설정
    BAR_Y = CANVAS_H - 70  # y 위치

    # HpBar 객체를 하나만 생성
    hp_bar = HpBar(
        x=CANVAS_W // 2,  # 화면 x축 중앙
        y=BAR_Y,
        width=BAR_W,
        height=BAR_H
    )


def exit():
    global background, p1, p2, hp_bar  # --- ❗️ 4. [수정] global 변수 ---
    del background
    del p1
    del p2
    del hp_bar  # --- ❗️ 5. [수정] 통합 HP 바 객체 삭제 ---


def handle_event(e):
    # (기존과 동일)
    global running
    if e.type == SDL_QUIT:
        running = False
    elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        running = False
    else:
        p1.handle_event(e)
        p2.handle_event(e)


def update(dt):
    # (기존과 동일)
    p1.update(dt)
    p2.update(dt)

    if check_collision(p1, p2):
        if p1.is_dive_kicking:
            p2.take_damage(1)
            print(f"P1 HITS! P2 HP: {p2.hp}")

        if p2.is_dive_kicking:
            p1.take_damage(1)
            print(f"P2 HITS! P1 HP: {p1.hp}")


def draw():
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)
    p1.draw()
    p2.draw()

    # --- ❗️ 6. [수정] HP 바 그리기 ---
    # hp_bar 객체 하나의 draw 함수에 p1과 p2의 hp를 모두 넘겨줌
    hp_bar.draw(p1.hp, p2.hp, 100)

    # (디버깅용 히트박스, 기존과 동일)
    # (l, b, r, t) = p1.get_hitbox()
    # draw_rectangle(l, b, r, t)
    # (l, b, r, t) = p2.get_hitbox()
    # draw_rectangle(l, b, r, t)

    update_canvas()


# --- 이 파일이 메인 파일로 실행될 때 ---
if __name__ == '__main__':
    framework.run(sys.modules[__name__])