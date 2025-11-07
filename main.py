from pico2d import *
import sys
import time

open_canvas(800, 600)

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

# --- 이미지 로드 ---
background = load_image('Stage.png')
character_stand = load_image('character1.png')      # '서있기' 이미지
character_jump_sheet = load_image('character1_jump.png') # '점프' 스프라이트 시트

# --- 컬러 키 설정 (필요하다면) ---
# 만약 시트 배경이 투명하지 않다면(예: 분홍색) 여기서 설정
# character_stand.colorkey_delta((255, 0, 255), 10)
# character_jump_sheet.colorkey_delta((255, 0, 255), 10)


# --- 점프 프레임 좌표 정의 (수정됨: 70x130 기준) ---
# (left, bottom, width, height)
JUMP_FRAME_CROUCH = (0, 0, 70, 130)   # 1번째 프레임 (left=0)
JUMP_FRAME_RISE = (70, 0, 70, 130)    # 2번째 프레임 (left=70)
JUMP_FRAME_FALL = (140, 0, 70, 130)   # 3번째 프레임 (left=140)

# --- 캐릭터의 '서있기' 기준 크기 (수정됨: 70x130 기준) ---
# character_stand.png 이미지의 원본 크기
base_sprite_w = 70
base_sprite_h = 130

# 그릴 때의 기준 크기 (2배 확대)
base_draw_w = base_sprite_w * 2
base_draw_h = base_sprite_h * 2

half_w = base_draw_w // 2
half_h = base_draw_h // 2

# 초기 위치
x = 400
ORIGINAL_GROUND = 90
# 발 위치를 유지하기 위해, 항상 '서있는' 캐릭터의 바닥을 기준으로 지면 Y를 계산
GROUND_Y = ORIGINAL_GROUND + (base_draw_h // 2)
y = GROUND_Y

# 이동 속도 (픽셀/초)
SPEED = 200

# 키 상태 추적(좌우만)
move_left = False
move_right = False

# 점프 관련
is_jumping = False
jump_velocity = 0.0
JUMP_SPEED = 500.0 * (2 ** 0.5)
GRAVITY = 1500.0

last_time = time.time()

running = True
while running:
    now = time.time()
    dt = now - last_time
    last_time = now

    # 입력 처리 (기존과 동일)
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
                if not is_jumping:
                    is_jumping = True
                    jump_velocity = JUMP_SPEED
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT or e.key == SDLK_a:
                move_left = False
            elif e.key == SDLK_RIGHT or e.key == SDLK_d:
                move_right = False

    # 수평 위치 업데이트 (기존과 동일)
    dx = 0
    if move_left:
        dx -= SPEED * dt
    if move_right:
        dx += SPEED * dt

    x += dx

    # 점프 물리 업데이트 (기존과 동일)
    if is_jumping:
        y += jump_velocity * dt
        jump_velocity -= GRAVITY * dt
        if y <= GROUND_Y:
            y = GROUND_Y
            is_jumping = False
            jump_velocity = 0.0

    # 캔버스 경계 내로 제한 (기존과 동일)
    if x < half_w:
        x = half_w
    if x > CANVAS_W - half_w:
        x = CANVAS_W - half_w
    if y > CANVAS_H - (base_draw_h // 2): # 천장 충돌 기준을 base_draw_h로 통일
        y = CANVAS_H - (base_draw_h // 2)

    # --- 렌더링 (로직 수정됨) ---
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    if is_jumping:
        # 점프 중일 때
        if jump_velocity > 0:
            frame_info = JUMP_FRAME_RISE
        else:
            frame_info = JUMP_FRAME_FALL

        # 점프 프레임의 원본 크기 (70, 130)
        current_sprite_w = frame_info[2]
        current_sprite_h = frame_info[3]
        # 점프 프레임을 그릴 크기 (2배 확대: 140, 260)
        current_draw_w = current_sprite_w * 2
        current_draw_h = current_sprite_h * 2

        character_jump_sheet.clip_draw(
            frame_info[0], frame_info[1], frame_info[2], frame_info[3], # (70,0,70,130) 또는 (140,0,70,130)
            int(x), int(y),
            current_draw_w, current_draw_h # 140, 260
        )
    else:
        # 땅에 있을 때
        character_stand.draw(int(x), int(y), base_draw_w, base_draw_h) # 140, 260

    update_canvas()
    # --- 렌더링 끝 ---

    delay(0.01)

close_canvas()