from pico2d import *
import time

open_canvas(800, 600)

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

# --- 이미지 로드 (수정됨) ---
background = load_image('Stage.png')
# P1
character_stand = load_image('character1.png')
character_jump_sheet = load_image('character1_jump.png')
character_divekick = load_image('character1_divekick.png')
character_walk_sheet = load_image('character1_walk.png')
# P2
character2_stand = load_image('character_2.png')
character2_walk_sheet = load_image('character_2_walk.png')
character2_jump_sheet = load_image('character2_jump.png')
# --- 새로 추가: P2 다이브킥 ---
character2_divekick = load_image('character2_divekick.png')

# --- 컬러 키 설정 (필요하다면) ---
# ...


# --- P1 점프 프레임 좌표 정의 (70x130 기준) ---
JUMP_FRAME_CROUCH = (0, 0, 70, 130)
JUMP_FRAME_RISE = (70, 0, 70, 130)
JUMP_FRAME_FALL = (140, 0, 70, 130)

# --- 픽셀 블리딩(깨짐) 방지용 패딩 ---
WALK_CLIP_PADDING = 1

# --- P1 걷기 프레임 좌표 정의 (64x130 기준) ---
WALK_FRAME_WIDTH = 64
WALK_FRAME_HEIGHT = 130
WALK_FRAMES = [
    (i * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT) for i in range(6)
]
NUM_WALK_FRAMES = len(WALK_FRAMES)
WALK_FPS = 10

# --- P2 걷기 프레임 좌표 정의 (66x130 기준) ---
WALK_FRAME_WIDTH_P2 = 66
WALK_FRAME_HEIGHT_P2 = 130
WALK_FRAMES_P2 = [
    (i * WALK_FRAME_WIDTH_P2, 0, WALK_FRAME_WIDTH_P2, WALK_FRAME_HEIGHT_P2) for i in range(8)
]
NUM_WALK_FRAMES_P2 = len(WALK_FRAMES_P2)
WALK_FPS_P2 = 10

# --- P2 점프 프레임 좌표 정의 (57x150 기준) ---
JUMP_FRAME_WIDTH_P2 = 57
JUMP_FRAME_HEIGHT_P2 = 150
JUMP_FRAME_RISE_P2 = (57, 0, JUMP_FRAME_WIDTH_P2, JUMP_FRAME_HEIGHT_P2)
JUMP_FRAME_FALL_P2 = (114, 0, JUMP_FRAME_WIDTH_P2, JUMP_FRAME_HEIGHT_P2)

# P2 기본 스프라이트 크기(프레임 단위) - '서있기' 기준
BASE_SPRITE_W_P2 = 66
BASE_SPRITE_H_P2 = 130
BASE_DRAW_W_P2 = BASE_SPRITE_W_P2 * 2
BASE_DRAW_H_P2 = BASE_SPRITE_H_P2 * 2

# P2 전용 클립 패딩
WALK_CLIP_PADDING_P2 = 0

# --- P1 '서있기' 기준 크기 (70x130 기준) ---
base_sprite_w = 70
base_sprite_h = 130
base_draw_w = base_sprite_w * 2
base_draw_h = base_sprite_h * 2
half_w = base_draw_w // 2
half_h = base_draw_h // 2

# --- P1 초기 위치 ---
x = half_w
ORIGINAL_GROUND = 90
GROUND_Y = ORIGINAL_GROUND + (base_draw_h // 2)
GROUND_Y_OFFSET = 20
CHARACTER_GROUND_Y = GROUND_Y - GROUND_Y_OFFSET
y = CHARACTER_GROUND_Y

# --- P2 초기 위치 ---
other_char_x = CANVAS_W - half_w
other_char_y = CHARACTER_GROUND_Y
x2 = other_char_x
y2 = other_char_y

# --- P2 상태 변수 ---
move_left2 = False
move_right2 = False
current_direction2 = -1
is_jumping2 = False
jump_velocity2 = 0.0
is_walking2 = False
walk_frame2 = 0.0
# --- 새로 추가: P2 다이브킥 ---
is_dive_kicking2 = False
DIVEKICK_SPEED_P2 = 700.0

# 이동 속도
SPEED = 200

# --- P1 상태 변수 ---
move_left = False
move_right = False
current_direction = 1
is_jumping = False
jump_velocity = 0.0
JUMP_SPEED = 500.0 * (2 ** 0.5)
GRAVITY = 1500.0
is_dive_kicking = False
DIVEKICK_SPEED_P1 = 700.0  # (변수 이름 DIVEKICK_SPEED -> DIVEKICK_SPEED_P1로 수정)
is_walking = False
walk_frame = 0.0

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
            # --- P1 조작: WASD ---
            elif e.key == SDLK_a:
                move_left = True
                current_direction = -1
            elif e.key == SDLK_d:
                move_right = True
                current_direction = 1
            elif e.key == SDLK_w or e.key == SDLK_SPACE:
                if not is_jumping:
                    is_jumping = True
                    is_walking = False
                    jump_velocity = JUMP_SPEED
            elif e.key == SDLK_s:
                if is_jumping and not is_dive_kicking:
                    is_dive_kicking = True
            # --- P2 조작: 화살표 ---
            elif e.key == SDLK_LEFT:
                move_left2 = True
                current_direction2 = -1
            elif e.key == SDLK_RIGHT:
                move_right2 = True
                current_direction2 = 1
            elif e.key == SDLK_UP:
                if not is_jumping2:
                    is_jumping2 = True
                    is_walking2 = False
                    jump_velocity2 = JUMP_SPEED
            # --- 새로 추가: P2 다이브킥 입력 ---
            elif e.key == SDLK_DOWN:
                if is_jumping2 and not is_dive_kicking2:
                    is_dive_kicking2 = True

        elif e.type == SDL_KEYUP:
            # P1 키 해제
            if e.key == SDLK_a: move_left = False
            if e.key == SDLK_d: move_right = False
            # P2 키 해제
            if e.key == SDLK_LEFT: move_left2 = False
            if e.key == SDLK_RIGHT: move_right2 = False

    # --- P1 위치 및 상태 업데이트 ---
    dx = 0
    if not is_jumping:
        if move_left:
            dx -= SPEED * dt
            is_walking = True
        elif move_right:
            dx += SPEED * dt
            is_walking = True
        else:
            is_walking = False
    else:
        if move_left: dx -= SPEED * dt
        if move_right: dx += SPEED * dt
    x += dx

    # --- P2 위치 및 상태 업데이트 ---
    dx2 = 0
    if not is_jumping2:
        if move_left2:
            dx2 -= SPEED * dt
            is_walking2 = True
        elif move_right2:
            dx2 += SPEED * dt
            is_walking2 = True
        else:
            is_walking2 = False
    else:
        if move_left2: dx2 -= SPEED * dt
        if move_right2: dx2 += SPEED * dt
    x2 += dx2

    # --- P1 점프 물리 (수정됨) ---
    if is_jumping:
        if is_dive_kicking:
            jump_velocity = -DIVEKICK_SPEED_P1  # (변수 이름 수정)
            y += jump_velocity * dt
        else:
            y += jump_velocity * dt
            jump_velocity -= GRAVITY * dt

        if y <= CHARACTER_GROUND_Y:
            y = CHARACTER_GROUND_Y
            is_jumping = False
            is_dive_kicking = False
            jump_velocity = 0.0
            if not move_left and not move_right:
                is_walking = False

    # --- P2 점프 물리 (수정됨) ---
    if is_jumping2:
        if is_dive_kicking2:
            # P2 다이브킥 중: 고정 속도 하강
            jump_velocity2 = -DIVEKICK_SPEED_P2
            y2 += jump_velocity2 * dt
        else:
            # P2 일반 점프 중: 중력 적용
            y2 += jump_velocity2 * dt
            jump_velocity2 -= GRAVITY * dt

        if y2 <= CHARACTER_GROUND_Y:
            y2 = CHARACTER_GROUND_Y
            is_jumping2 = False
            is_dive_kicking2 = False  # 착지 시 다이브킥 해제
            jump_velocity2 = 0.0
            if not move_left2 and not move_right2:
                is_walking2 = False

    # 캔버스 경계 제한
    if x < half_w: x = half_w
    if x > CANVAS_W - half_w: x = CANVAS_W - half_w
    if x2 < half_w: x2 = half_w
    if x2 > CANVAS_W - half_w: x2 = CANVAS_W - half_w
    if y > CANVAS_H - (base_draw_h // 2): y = CANVAS_H - (base_draw_h // 2)
    if y2 > CANVAS_H - (base_draw_h // 2): y2 = CANVAS_H - (base_draw_h // 2)

    # --- 애니메이션 프레임 업데이트 ---
    if is_walking:
        walk_frame = (walk_frame + WALK_FPS * dt) % NUM_WALK_FRAMES
    if is_walking2:
        walk_frame2 = (walk_frame2 + WALK_FPS_P2 * dt) % NUM_WALK_FRAMES_P2

    # --- 렌더링 ---
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    # === P1 그리기 ===
    current_sheet = None
    frame_info = None
    draw_x = int(x)
    draw_y = int(y)

    if is_jumping:
        if is_dive_kicking:
            current_sheet = character_divekick
            current_sprite_w = 114
            current_sprite_h = 130
        else:
            current_sheet = character_jump_sheet
            frame_info = JUMP_FRAME_RISE if jump_velocity > 0 else JUMP_FRAME_FALL
            current_sprite_w = frame_info[2]
            current_sprite_h = frame_info[3]
    elif is_walking:
        current_sheet = character_walk_sheet
        raw_frame = WALK_FRAMES[int(walk_frame)]
        clip_x = raw_frame[0] + WALK_CLIP_PADDING
        clip_w = max(1, raw_frame[2] - 2 * WALK_CLIP_PADDING)
        frame_info = (clip_x, raw_frame[1], clip_w, raw_frame[3])
        current_sprite_w = clip_w
        current_sprite_h = raw_frame[3]
    else:  # 서있기
        current_sheet = character_stand
        current_sprite_w = base_sprite_w
        current_sprite_h = base_sprite_h

    draw_w = current_sprite_w * 2
    draw_h = current_sprite_h * 2

    if frame_info:
        if current_direction == -1:
            current_sheet.clip_composite_draw(frame_info[0], frame_info[1], frame_info[2], frame_info[3], 0, 'h',
                                              draw_x, draw_y, draw_w, draw_h)
        else:
            current_sheet.clip_draw(frame_info[0], frame_info[1], frame_info[2], frame_info[3], draw_x, draw_y, draw_w,
                                    draw_h)
    elif current_sheet:
        if current_direction == -1:
            current_sheet.composite_draw(0, 'h', draw_x, draw_y, draw_w, draw_h)
        else:
            current_sheet.draw(draw_x, draw_y, draw_w, draw_h)

    # === P2 그리기 (수정됨) ===
    current_sheet2 = None
    frame_info2 = None
    other_x = int(x2)
    other_y = int(y2)

    if is_jumping2:
        if is_dive_kicking2:
            # P2 다이브킥 상태
            current_sheet2 = character2_divekick
            current_sprite_w2 = current_sheet2.w  # 이미지 원본 크기
            current_sprite_h2 = current_sheet2.h
        else:
            # P2 일반 점프 상태
            current_sheet2 = character2_jump_sheet
            if jump_velocity2 > 0:
                frame_info2 = JUMP_FRAME_RISE_P2
            else:
                frame_info2 = JUMP_FRAME_FALL_P2
            current_sprite_w2 = frame_info2[2]
            current_sprite_h2 = frame_info2[3]
    elif is_walking2:
        # P2 걷기 상태
        current_sheet2 = character2_walk_sheet
        raw_frame2 = WALK_FRAMES_P2[int(walk_frame2)]
        clip_x2 = raw_frame2[0] + WALK_CLIP_PADDING_P2
        clip_y2 = raw_frame2[1]
        clip_w2 = max(1, raw_frame2[2] - 2 * WALK_CLIP_PADDING_P2)
        clip_h2 = raw_frame2[3]
        frame_info2 = (clip_x2, clip_y2, clip_w2, clip_h2)
        current_sprite_w2 = clip_w2
        current_sprite_h2 = clip_h2
    else:  # P2 서있기 상태
        current_sheet2 = character2_stand
        current_sprite_w2 = BASE_SPRITE_W_P2
        current_sprite_h2 = BASE_SPRITE_H_P2

    # P2 그릴 크기 (현재 프레임 기준 2배)
    other_w = current_sprite_w2 * 2
    other_h = current_sprite_h2 * 2

    # P2 그리기 (방향 전환)
    if frame_info2:  # 걷기 또는 점프 (clip_draw)
        if current_direction2 == -1:
            current_sheet2.clip_composite_draw(frame_info2[0], frame_info2[1], frame_info2[2], frame_info2[3], 0, 'h',
                                               other_x, other_y, other_w, other_h)
        else:
            current_sheet2.clip_draw(frame_info2[0], frame_info2[1], frame_info2[2], frame_info2[3], other_x, other_y,
                                     other_w, other_h)
    elif current_sheet2:  # 서있기 또는 다이브킥 (draw)
        if current_direction2 == -1:
            current_sheet2.composite_draw(0, 'h', other_x, other_y, other_w, other_h)
        else:
            current_sheet2.draw(other_x, other_y, other_w, other_h)

    update_canvas()
    # --- 렌더링 끝 ---

    delay(0.01)

close_canvas()