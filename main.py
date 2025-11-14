# main.py

import framework  # 만들어둔 프레임워크를 불러옴
from pico2d import *
from character import Character  # 만들어둔 캐릭터 클래스를 불러옴
from constants import *  # 만들어둔 상수를 모두 불러옴

# main.py에서만 사용할 변수
background = None
p1 = None
p2 = None
running = True  # 게임 루프 실행 여부


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


def draw():
    """모든 게임 객체를 화면에 그립니다."""
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)
    p1.draw()
    p2.draw()
    update_canvas()


# --- 이 파일이 메인 파일로 실행될 때 ---
if __name__ == '__main__':
    framework.run(sys.modules[__name__])