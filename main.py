from pico2d import *
import sys
import time

open_canvas(800, 600)

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

# --- 이미지 로드 ---
background = load_image('Stage.png')
character_stand = load_image('character1.png')
character_jump_sheet = load_image('character1_jump.png')
# --- 새로 추가: 다이브킥 시트 ---
character_divekick_sheet = load_image('character1_divekick.png')

# --- 컬러 키 설정 (필요하다면) ---
# character_divekick_sheet.colorkey_delta((255, 0, 255), 10)


# --- 점프 프레임 좌표 정의 (70x130 기준) ---
JUMP_FRAME_CROUCH = (0, 0, 70, 130)
JUMP_FRAME_RISE = (70, 0, 70, 130)
JUMP_FRAME_FALL = (140, 0, 70, 130)

# --- 새로 추가: 다이브킥 프레임 좌표 정의 ---
# (left, bottom, width, height)
# 1프레임: 88x130, left=0
# 2프레임: 68x130, left=88
# 3프레임: 114x130, left=88+68=156
DIVEKICK_FRAME_1 = (0, 0, 88, 130)
DIVEKICK_FRAME_2 = (88, 0, 68, 130)
DIVEKICK_FRAME_3 = (156, 0, 114, 130)
# 애니메이션을 위한 프레임 리스트
DIVEKICK_FRAMES = [DIVEKICK_FRAME_1, DIVEKICK_FRAME_2, DIVEKICK_FRAME_3]

# --- 캐릭터의 '서있기' 기준 크기 (70x130 기준) ---
base_sprite_w = 70
base_sprite_h = 130
base_draw_w = base_sprite_w * 2
base_draw_h = base_sprite_h * 2
half_w = base_draw_w // 2
half_h = base_draw_h // 2

# 초기 위치
x = 400
ORIGINAL_GROUND = 90
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

# --- 새로 추가: 다이브킥 관련 ---
is_dive_kicking = False
DIVEKICK_SPEED = 900.0  # 다이브킥 하강 속도 (픽셀/초)
divekick_frame = 0.0  # 다이브킥 애니메이션 프레임 인덱스
DIVEKICK_FPS = 10  # 다이브킥 애니메이션 속도 (초당 프레임)

last_time = time.time()

running = True
while running:
    now = time.time()
    dt = now - last_time
    last_time = now

    # --- 입력 처리 (수정됨) ---
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
            # --- 새로 추가: 다이브킥 입력 ---
            elif e.key == SDLK_DOWN:
                if is_jumping and not is_dive_kicking:
                    # 점프 중일 때만 다이브킥 발동
                    is_dive_kicking = True
                    divekick_frame = 0.0  # 애니메이션 0번 프레임부터 시작

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

    # --- 점프 물리 업데이트 (수정됨) ---
    if is_jumping:
        if is_dive_kicking:
            # 다이브킥 중: 중력 무시, 고정 속도로 하강
            jump_velocity = -DIVEKICK_SPEED  # 속도를 강제로 아래로 고정
            y += jump_velocity * dt
        else:
            # 일반 점프 중: 중력 적용
            y += jump_velocity * dt
            jump_velocity -= GRAVITY * dt

        # 착지 체크
        if y <= GROUND_Y:
            y = GROUND_Y
            is_jumping = False
            is_dive_kicking = False  # 착지하면 다이브킥 상태 해제
            jump_velocity = 0.0

    # 캔버스 경계 내로 제한 (기존과 동일)
    if x < half_w: x = half_w
    if x > CANVAS_W - half_w: x = CANVAS_W - half_w
    if y > CANVAS_H - (base_draw_h // 2): y = CANVAS_H - (base_draw_h // 2)

    # --- 렌더링 (로직 수정됨) ---
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    if is_jumping:
        if is_dive_kicking:
            # --- 다이브킥 그리기 ---
            # 애니메이션 프레임 업데이트 (dt * FPS 만큼 증가)
            divekick_frame = (divekick_frame + DIVEKICK_FPS * dt) % 3  # 0, 1, 2 반복
            frame_index = int(divekick_frame)
            frame_info = DIVEKICK_FRAMES[frame_index]  # 현재 프레임 정보

            # 현재 프레임의 원본 크기 (88, 68, 114 중 하나)
            current_sprite_w = frame_info[2]
            current_sprite_h = frame_info[3]
            # 그릴 크기 (2배 확대)
            current_draw_w = current_sprite_w * 2
            current_draw_h = current_sprite_h * 2

            character_divekick_sheet.clip_draw(
                frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                int(x), int(y),
                current_draw_w, current_draw_h
            )
        else:
            # --- 일반 점프 그리기 ---
            if jump_velocity > 0:
                frame_info = JUMP_FRAME_RISE
            else:
                frame_info = JUMP_FRAME_FALL

            current_sprite_w = frame_info[2]
            current_sprite_h = frame_info[3]
            current_draw_w = current_sprite_w * 2
            current_draw_h = current_sprite_h * 2

            character_jump_sheet.clip_draw(
                frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                int(x), int(y),
                current_draw_w, current_draw_h
            )
    else:
        # --- 땅에 있을 때 그리기 ---
        character_stand.draw(int(x), int(y), base_draw_w, base_draw_h)

    update_canvas()
    # --- 렌더링 끝 ---

    delay(0.01)

close_canvas()