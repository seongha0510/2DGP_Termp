from pico2d import *
import time

open_canvas(800, 600)

# 캔버스 크기 상수
CANVAS_W, CANVAS_H = 800, 600

# --- 이미지 로드 (수정됨) ---
background = load_image('Stage.png')
character_stand = load_image('character1.png')
character_jump_sheet = load_image('character1_jump.png')
character_divekick = load_image('character1_divekick.png')
# --- 새로 추가: 걷기 스프라이트 시트 ---
character_walk_sheet = load_image('character1_walk.png')  # 6프레임 걷기 시트
# --- 새로 추가: 상대 캐릭터 ---
character2 = load_image('character_2.png')  # 반대편에서 마주볼 캐릭터

# --- 컬러 키 설정 (필요하다면) ---
# character_walk_sheet.colorkey_delta((255, 0, 255), 10)


# --- 점프 프레임 좌표 정의 (70x130 기준) ---
JUMP_FRAME_CROUCH = (0, 0, 70, 130)
JUMP_FRAME_RISE = (70, 0, 70, 130)
JUMP_FRAME_FALL = (140, 0, 70, 130)

# --- 새로 추가: 걷기 프레임 좌우 패딩 (프레임 경계 겹침 방지) ---
WALK_CLIP_PADDING = 1

# --- 새로 추가: 걷기 프레임 좌표 정의 (66x130 기준) ---
# (left, bottom, width, height)
WALK_FRAME_WIDTH = 64
WALK_FRAME_HEIGHT = 130
WALK_FRAMES = [
    (0 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT),  # 1번째 프레임
    (1 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT),  # 2번째 프레임
    (2 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT),  # 3번째 프레임
    (3 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT),  # 4번째 프레임
    (4 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT),  # 5번째 프레임
    (5 * WALK_FRAME_WIDTH, 0, WALK_FRAME_WIDTH, WALK_FRAME_HEIGHT)  # 6번째 프레임
]
NUM_WALK_FRAMES = len(WALK_FRAMES)
WALK_FPS = 10  # 걷기 애니메이션 속도 (초당 프레임)

# --- 캐릭터의 '서있기' 기준 크기 (70x130 기준) ---
base_sprite_w = 70  # 서있을 때 기준이므로 70x130 유지
base_sprite_h = 130
base_draw_w = base_sprite_w * 2
base_draw_h = base_sprite_h * 2
half_w = base_draw_w // 2
half_h = base_draw_h // 2

# 초기 위치
x = half_w  # main 캐릭터 시작: 왼쪽 끝에 배치
ORIGINAL_GROUND = 90
GROUND_Y = ORIGINAL_GROUND + (base_draw_h // 2)
# main 캐릭터 및 character2의 실제 착지 높이(화면에 더 낮게 보이도록 오프셋 적용)
GROUND_Y_OFFSET = 20  # 내려보일 픽셀 수, 필요하면 조정
CHARACTER_GROUND_Y = GROUND_Y - GROUND_Y_OFFSET
# main 캐릭터 시작 Y
y = CHARACTER_GROUND_Y

# --- 다른 캐릭터 시작 위치: 오른쪽 끝에 고정 ---
other_char_x = CANVAS_W - half_w
# 다른 캐릭터를 main과 동일한 높이로 설정
other_char_y = CHARACTER_GROUND_Y

# --- character2 상태 변수 (이동/점프) ---
x2 = other_char_x
y2 = other_char_y
move_left2 = False
move_right2 = False
current_direction2 = -1  # 오른쪽 끝에 있으니 왼쪽을 바라보게 기본값 -1
is_jumping2 = False
jump_velocity2 = 0.0

# 이동 속도 (픽셀/초)
SPEED = 200

# 키 상태 추적(좌우만)
move_left = False
move_right = False
# --- 새로 추가: 현재 캐릭터가 바라보는 방향 ---
# 1 = 오른쪽, -1 = 왼쪽
current_direction = 1

# 점프 관련
is_jumping = False
jump_velocity = 0.0
JUMP_SPEED = 500.0 * (2 ** 0.5)
GRAVITY = 1500.0

# 다이브킥 관련
is_dive_kicking = False
DIVEKICK_SPEED = 700.0

# --- 새로 추가: 걷기 관련 ---
is_walking = False  # 현재 걷고 있는지 여부
walk_frame = 0.0  # 현재 걷기 애니메이션 프레임 인덱스

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
            # --- character_1 조작: WASD ---
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
                # main 캐릭터 다이브킥: 점프 중일 때만 발동
                if is_jumping and not is_dive_kicking:
                    is_dive_kicking = True
            # --- character_2 조작: 화살표 ---
            elif e.key == SDLK_LEFT:
                move_left2 = True
                current_direction2 = -1
            elif e.key == SDLK_RIGHT:
                move_right2 = True
                current_direction2 = 1
            elif e.key == SDLK_UP:
                if not is_jumping2:
                    is_jumping2 = True
                    jump_velocity2 = JUMP_SPEED

        elif e.type == SDL_KEYUP:
            # character_1 키 해제
            if e.key == SDLK_a:
                move_left = False
            elif e.key == SDLK_d:
                move_right = False
            if not move_left and not move_right:
                is_walking = False
            # character_2 키 해제
            if e.key == SDLK_LEFT:
                move_left2 = False
            elif e.key == SDLK_RIGHT:
                move_right2 = False

    # --- 수평 위치 업데이트 (수정됨) ---
    dx = 0
    if move_left:
        dx -= SPEED * dt
        is_walking = True
    if move_right:
        dx += SPEED * dt
        is_walking = True

    # character2 수평 이동
    dx2 = 0
    if move_left2:
        dx2 -= SPEED * dt
    if move_right2:
        dx2 += SPEED * dt

    # 두 키 모두 눌려있지 않으면 걷기 아님 (점프 중이 아닐 때만)
    if not (move_left or move_right) and not is_jumping:
        is_walking = False

    x += dx
    x2 += dx2

    # --- 점프 물리 업데이트 (기존과 동일) ---
    if is_jumping:
        if is_dive_kicking:
            jump_velocity = -DIVEKICK_SPEED
            y += jump_velocity * dt
        else:
            y += jump_velocity * dt
            jump_velocity -= GRAVITY * dt

        # 착지 시 실제 착지 높이로 복구
        if y <= CHARACTER_GROUND_Y:
            y = CHARACTER_GROUND_Y
            is_jumping = False
            is_dive_kicking = False
            is_walking = False  # 착지하면 걷기 멈춤
            jump_velocity = 0.0

    # character2 점프 물리
    if is_jumping2:
        y2 += jump_velocity2 * dt
        jump_velocity2 -= GRAVITY * dt
        if y2 <= CHARACTER_GROUND_Y:
            y2 = CHARACTER_GROUND_Y
            is_jumping2 = False
            jump_velocity2 = 0.0

    # 캔버스 경계 내로 제한 (기존과 동일)
    if x < half_w: x = half_w
    if x > CANVAS_W - half_w: x = CANVAS_W - half_w
    if x2 < half_w: x2 = half_w
    if x2 > CANVAS_W - half_w: x2 = CANVAS_W - half_w
    if y > CANVAS_H - (base_draw_h // 2): y = CANVAS_H - (base_draw_h // 2)
    if y2 > CANVAS_H - (base_draw_h // 2): y2 = CANVAS_H - (base_draw_h // 2)

    # --- 걷기 애니메이션 프레임 업데이트 (새로 추가) ---
    if is_walking:
        walk_frame = (walk_frame + WALK_FPS * dt) % NUM_WALK_FRAMES

    # --- 렌더링 (수정됨) ---
    clear_canvas()
    background.draw(CANVAS_W // 2, CANVAS_H // 2, CANVAS_W, CANVAS_H)

    # 그릴 스프라이트 시트와 프레임 정보 결정
    current_sheet = None
    frame_info = None

    if is_jumping:
        if is_dive_kicking:
            current_sheet = character_divekick  # 단일 이미지이므로 시트 아님
            current_sprite_w = 114  # 다이브킥 이미지의 원본 폭
            current_sprite_h = 130  # 다이브킥 이미지의 원본 높이
        else:
            current_sheet = character_jump_sheet
            if jump_velocity > 0:
                frame_info = JUMP_FRAME_RISE
            else:
                frame_info = JUMP_FRAME_FALL
            current_sprite_w = frame_info[2]
            current_sprite_h = frame_info[3]
    elif is_walking:
        current_sheet = character_walk_sheet
        # 원본 프레임에서 좌우 패딩만큼 내부로 잘라서 사용
        raw_frame = WALK_FRAMES[int(walk_frame)]  # (left, bottom, width, height)
        clip_x = raw_frame[0] + WALK_CLIP_PADDING
        clip_y = raw_frame[1]
        clip_w = max(1, raw_frame[2] - 2 * WALK_CLIP_PADDING)  # 좌우 각각 패딩 제거
        clip_h = raw_frame[3]
        frame_info = (clip_x, clip_y, clip_w, clip_h)
        current_sprite_w = clip_w  # 잘라낸 폭 사용
        current_sprite_h = clip_h  # 프레임 높이
    else:  # 땅에 있고 걷지 않을 때
        current_sheet = character_stand  # 단일 이미지
        current_sprite_w = base_sprite_w  # 서있기 이미지의 원본 폭 (70)
        current_sprite_h = base_sprite_h  # 서있기 이미지의 원본 높이 (130)

    # 현재 상태에 따른 그리기
    draw_x = int(x)
    draw_y = int(y)
    draw_w = current_sprite_w * 2
    draw_h = current_sprite_h * 2

    # --- 좌우 반전 처리 ---
    # character_stand, character_jump_sheet, character_divekick_sheet 등
    # draw_2x(), clip_draw_2x()는 pico2d에 없으므로 clip_composite_draw / composite_draw 사용

    if frame_info:  # 시트에서 자르는 경우 (점프, 걷기)
        if current_sheet == character_jump_sheet:  # 점프는 방향에 따라 반전 처리
            if current_direction == -1:
                current_sheet.clip_composite_draw(
                    frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                    0, 'h', draw_x, draw_y, draw_w, draw_h
                )
            else:
                current_sheet.clip_draw(
                    frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                    draw_x, draw_y, draw_w, draw_h
                )
        else:  # 걷기 (current_sheet == character_walk_sheet)
            # 걷기는 좌우 방향에 따라 반전 처리 (clip_composite_draw 사용)
            if current_direction == -1:
                # 수평 반전
                current_sheet.clip_composite_draw(
                    frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                    0, 'h', draw_x, draw_y, draw_w, draw_h
                )
            else:
                current_sheet.clip_draw(
                    frame_info[0], frame_info[1], frame_info[2], frame_info[3],
                    draw_x, draw_y, draw_w, draw_h
                )
    elif current_sheet == character_divekick:  # 다이브킥
        if current_direction == -1:
            # 전체 이미지를 수평 반전해서 그리기
            current_sheet.composite_draw(0, 'h', draw_x, draw_y, draw_w, draw_h)
        else:
            current_sheet.draw(draw_x, draw_y, draw_w, draw_h)
    elif current_sheet == character_stand:  # 서있기
        if current_direction == -1:
            current_sheet.composite_draw(0, 'h', draw_x, draw_y, draw_w, draw_h)
        else:
            current_sheet.draw(draw_x, draw_y, draw_w, draw_h)

    # --- 새로 추가: 반대편의 character_2를 오른쪽 끝 고정 위치에 그리기 ---
    other_x = int(x2)
    other_y = int(y2)
    other_w = base_draw_w
    other_h = base_draw_h
    # character2는 자신의 방향(current_direction2)으로 그리기
    if current_direction2 == -1:
        character2.composite_draw(0, 'h', other_x, other_y, other_w, other_h)
    else:
        character2.draw(other_x, other_y, other_w, other_h)

    update_canvas()
    # --- 렌더링 끝 ---

    delay(0.01)

close_canvas()