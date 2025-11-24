# play_state.py

import framework
import sys
from pico2d import *
from character import Character
from constants import *
from hp_bar import HpBar
from effect import Explosion  # 이펙트 클래스

# play_state에서 사용할 변수들
background = None
p1 = None
p2 = None
hp_bar = None
font = None
game_timer = 60.0
running = True
effects = []  # 이펙트 리스트
collision_cooldown = 0.0  # ❗️ [추가] 타격 쿨타임 변수


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
    global background, p1, p2, hp_bar, font, game_timer, effects, collision_cooldown

    background = load_image('Stage.png')

    # 폰트 로드
    font = load_font('VITRO_CORE_TTF.ttf', 30)

    # 타이머, 이펙트 리스트, 쿨타임 초기화
    game_timer = 60.0
    effects = []
    collision_cooldown = 0.0  # ❗️ 초기화

    # --- P1 설정 ---
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

    # --- P2 설정 ---
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

    # 캐릭터 객체 생성
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

    # HP 바 생성
    BAR_W, BAR_H = 600, 50
    BAR_Y = CANVAS_H - 70
    hp_bar = HpBar(
        x=CANVAS_W // 2,
        y=BAR_Y,
        width=BAR_W,
        height=BAR_H
    )


def exit():
    global background, p1, p2, hp_bar, font, effects
    del background
    del p1
    del p2
    del hp_bar
    del font
    del effects


def handle_event(e):
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        framework.quit()
    else:
        p1.handle_event(e)
        p2.handle_event(e)


def update(dt):
    global game_timer, effects, collision_cooldown

    # 타이머 업데이트
    if game_timer > 0:
        game_timer -= dt
    else:
        game_timer = 0

    # ❗️ [추가] 쿨타임 감소
    if collision_cooldown > 0:
        collision_cooldown -= dt

    # 캐릭터 업데이트
    p1.update(dt)
    p2.update(dt)

    # 이펙트 업데이트 및 완료된 이펙트 제거
    for effect in effects:
        effect.update(dt)
    effects = [e for e in effects if not e.finished]

    # --- 충돌 판정 (데미지 & 이펙트) ---
    # ❗️ 쿨타임(collision_cooldown)이 0 이하일 때만 데미지를 줍니다.
    if check_collision(p1, p2) and collision_cooldown <= 0:
        collision_happened = False

        # 충돌 위치 계산 (두 캐릭터의 중간)
        hit_x = (p1.x + p2.x) / 2
        hit_y = (p1.y + p2.y) / 2

        if p1.is_dive_kicking:
            p2.take_damage(4)
            collision_happened = True
            print(f"P1 HITS! P2 HP: {p2.hp}")

        if p2.is_dive_kicking:
            p1.take_damage(1)
            collision_happened = True
            print(f"P2 HITS! P1 HP: {p1.hp}")

        # 충돌 시 이펙트 생성 및 쿨타임 설정
        if collision_happened:
            new_effect = Explosion(hit_x, hit_y)
            effects.append(new_effect)

            # ❗️ [추가] 한 번 때리면 0.5초 동안 타격 판정 중지
            collision_cooldown = 0.05

            # --- 충돌 판정 (밀어내기) ---
    # ❗️ 밀어내기는 쿨타임과 상관없이 항상 작동해야 통과하지 못합니다.
    if check_collision(p1, p2):
        l1, b1, r1, t1 = p1.get_hitbox()
        l2, b2, r2, t2 = p2.get_hitbox()

        overlap_x = min(r1, r2) - max(l1, l2)

        if overlap_x > 0:
            push_amount = overlap_x / 2

            if p1.x < p2.x:
                p1.x -= push_amount
                p2.x += push_amount
            else:
                p1.x += push_amount
                p2.x -= push_amount

            p1.x = max(0, min(CANVAS_W, p1.x))
            p2.x = max(0, min(CANVAS_W, p2.x))


def draw():
    clear_canvas()

    # 1. 배경
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    # 2. 캐릭터
    p1.draw()
    p2.draw()

    # 3. 이펙트 (캐릭터 위에 그림)
    for effect in effects:
        effect.draw()

    # 4. HP 바
    hp_bar.draw(p1.hp, p2.hp, 100)

    # 5. 타이머 텍스트
    timer_int = max(0, int(game_timer))
    timer_text = f"{timer_int:02d}"

    text_x = hp_bar.x - 21
    text_y = hp_bar.y - 2
    font.draw(text_x, text_y, timer_text, (255, 255, 255))

    # 6. 디버그용 히트박스 (필요하면 주석 해제)
    # (l, b, r, t) = p1.get_hitbox()
    # draw_rectangle(l, b, r, t)
    # (l, b, r, t) = p2.get_hitbox()
    # draw_rectangle(l, b, r, t)

    update_canvas()