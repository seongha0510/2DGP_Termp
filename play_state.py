# play_state.py

import framework
import sys
from pico2d import *
from character import Character
from constants import *
from hp_bar import HpBar

# main.py에서만 사용할 변수
background = None
p1 = None
p2 = None
hp_bar = None
font = None  # --- ❗️ [추가] 폰트 객체를 담을 변수 ---
game_timer = 60.0  # --- ❗️ [추가] 게임 타이머 (60초) ---
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
    # --- ❗️ [수정] global 변수에 font, game_timer 추가 ---
    global background, p1, p2, hp_bar, font, game_timer

    background = load_image('Stage.png')

    # --- ❗️ [추가] 폰트 로드 ---
    # (프로젝트 폴더에 'font.ttf' 파일이 있어야 합니다. 폰트 크기는 30으로 설정)
    font = load_font('VITRO_CORE_TTF.ttf', 30)

    # --- ❗️ [추가] 타이머 초기화 ---
    game_timer = 60.0

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

    # --- HP 바 객체 생성 (기존과 동일) ---
    # (참고: main.py와 hp_bar.py의 너비(600)와 높이(50) 설정이
    # 이전 대화(760)와 다릅니다. 업로드된 파일을 기준으로 600, 50으로 진행합니다.)
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
    # --- ❗️ [수정] global 변수에 font 추가 ---
    global background, p1, p2, hp_bar, font
    del background
    del p1
    del p2
    del hp_bar
    del font  # --- ❗️ [추가] 폰트 객체 삭제 ---


def handle_event(e):
    # (기존과 동일)
    global running
    if e.type == SDL_QUIT:
        framework.quit()
    elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        framework.quit()
    else:
        p1.handle_event(e)
        p2.handle_event(e)


def update(dt):
    # global 변수
    global game_timer

    # 1. 타이머 업데이트
    if game_timer > 0:
        game_timer -= dt
    else:
        game_timer = 0
        # (타임오버 로직이 필요하면 여기에 추가)

    # 2. 캐릭터 업데이트
    p1.update(dt)
    p2.update(dt)

    # 3. 데미지 판정 (기존 로직)
    if check_collision(p1, p2):
        if p1.is_dive_kicking:
            p2.take_damage(1)
            print(f"P1 HITS! P2 HP: {p2.hp}")

        if p2.is_dive_kicking:
            p1.take_damage(1)
            print(f"P2 HITS! P1 HP: {p1.hp}")

    # --- ❗️ [추가] 충돌 시 서로 밀어내기 (통과 방지) ---
    # 데미지 판정 후에도 여전히 겹쳐 있다면, 위치를 강제로 조정합니다.
    if check_collision(p1, p2):
        # 각 캐릭터의 히트박스 가져오기
        l1, b1, r1, t1 = p1.get_hitbox()
        l2, b2, r2, t2 = p2.get_hitbox()

        # 겹친 가로 길이(overlap_x) 계산
        # (두 박스 사이의 교차 영역 너비를 구합니다)
        overlap_x = min(r1, r2) - max(l1, l2)

        if overlap_x > 0:
            # 겹친 만큼을 반으로 나눠서 서로 반대쪽으로 밀어냄
            push_amount = overlap_x / 2

            # P1이 P2보다 왼쪽에 있으면 -> P1은 왼쪽, P2는 오른쪽으로 밈
            if p1.x < p2.x:
                p1.x -= push_amount
                p2.x += push_amount
            # P1이 P2보다 오른쪽에 있으면 -> P1은 오른쪽, P2는 왼쪽으로 밈
            else:
                p1.x += push_amount
                p2.x -= push_amount

            # (선택 사항) 밀려난 후 화면 밖으로 나가지 않게 막기
            # P1 화면 제한
            p1.x = max(0, min(CANVAS_W, p1.x))
            # P2 화면 제한
            p2.x = max(0, min(CANVAS_W, p2.x))

def draw():
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)
    p1.draw()
    p2.draw()

    # HP 바 그리기
    hp_bar.draw(p1.hp, p2.hp, 100)

    # --- ❗️ [추가] 타이머 그리기 ---
    timer_int = max(0, int(game_timer))  # 0초 이하로 내려가지 않게
    timer_text = f"{timer_int:02d}"  # 항상 2자리로 표시 (예: 60, 09, 00)

    # HP 바의 중심 좌표(hp_bar.x, hp_bar.y)를 기준으로 텍스트 중앙 정렬
    # (폰트 크기 30 기준, 2글자 너비 약 30px, 높이 30px 가정)
    text_x = hp_bar.x - 21  # (30px 너비의 절반)
    text_y = hp_bar.y - 2  # (30px 높이의 절반)

    # 흰색(255, 255, 255)으로 텍스트 그리기
    font.draw(text_x, text_y, timer_text, (255, 255, 255))
    # --- [추가] 끝 ---

    # (디버깅용 히트박스, 기존과 동일)
    (l, b, r, t) = p1.get_hitbox()
    draw_rectangle(l, b, r, t)
    (l, b, r, t) = p2.get_hitbox()
    draw_rectangle(l, b, r, t)

    update_canvas()


# --- 이 파일이 메인 파일로 실행될 때 ---
#if __name__ == '__main__':
    #framework.run(sys.modules[__name__])