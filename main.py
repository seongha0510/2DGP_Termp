from pico2d import *
import sys
import time

open_canvas(800, 600)

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

background = load_image('Stage.png')
character = load_image('character1.png')

# 스프라이트 크기
sprite_w = character.w if hasattr(character, 'w') else character.get_width()
sprite_h = character.h if hasattr(character, 'h') else character.get_height()
half_w = sprite_w // 2
half_h = sprite_h // 2

# 초기 위치
x = 400   # 중앙
# y는 스프라이트가 서있는 바닥 Y좌표(중심 기준)
GROUND_Y = 90
y = GROUND_Y

# 이동 속도 (픽셀/초)
SPEED = 200

# 키 상태 추적(좌우만)
move_left = False
move_right = False

# 점프 관련
is_jumping = False
jump_velocity = 0.0
JUMP_SPEED = 500.0   # 점프 초기 속도(픽셀/초)
GRAVITY = 1500.0     # 중력 가속도(픽셀/초^2)

last_time = time.time()

running = True
while running:
    now = time.time()
    dt = now - last_time
    last_time = now

    # 입력 처리
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_LEFT or e.key == SDLK_a:
                move_left = True
            elif e.key == SDLK_RIGHT or e.key == SDLK_d:
                move_right = True
            elif (e.key == SDLK_UP) or (e.key == SDLK_SPACE):
                # 점프 시작 (이미 점프 중이면 무시)
                if not is_jumping:
                    is_jumping = True
                    jump_velocity = JUMP_SPEED
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT or e.key == SDLK_a:
                move_left = False
            elif e.key == SDLK_RIGHT or e.key == SDLK_d:
                move_right = False

    # 수평 위치 업데이트 (시간 기반)
    dx = 0
    if move_left:
        dx -= SPEED * dt
    if move_right:
        dx += SPEED * dt

    x += dx

    # 점프 물리 업데이트
    if is_jumping:
        y += jump_velocity * dt
        jump_velocity -= GRAVITY * dt
        # 착지 체크
        if y <= GROUND_Y:
            y = GROUND_Y
            is_jumping = False
            jump_velocity = 0.0

    # 캔버스 경계 내로 제한 (수평은 스프라이트 반폭, 수직은 바닥~상단)
    if x < half_w:
        x = half_w
    if x > CANVAS_W - half_w:
        x = CANVAS_W - half_w
    if y > CANVAS_H - half_h:
        y = CANVAS_H - half_h

    # 렌더링
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)
    character.draw(int(x), int(y))
    update_canvas()

    delay(0.01)

close_canvas()
