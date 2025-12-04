# character.py

from pico2d import *
from constants import *


class Character:
    def __init__(self, x, direction, keys, assets, frames, rules):
        self.x, self.y = x, CHARACTER_GROUND_Y
        self.current_direction = direction

        # 상태 변수들
        self.move_left = False
        self.move_right = False
        self.is_jumping = False
        self.is_dive_kicking = False
        self.is_walking = False
        # ❗️ [추가] 죽었는지 확인하는 변수
        self.is_dead = False

        self.jump_velocity = 0.0

        # 애니메이션 관련
        self.walk_frame = 0.0
        # ❗️ [추가] 죽는 모션 프레임
        self.dead_frame = 0.0

        self.keys = keys
        self.assets = assets
        self.frames = frames
        self.rules = rules

        self.divekick_speed = self.rules.get('dive_speed', 700.0)
        self.hp = 100

    def handle_event(self, event):
        # ❗️ [추가] 죽었으면 키 입력 무시
        if self.is_dead:
            return

        if event.type == SDL_KEYDOWN:
            if event.key == self.keys['left']:
                self.move_left = True
                self.current_direction = -1
            elif event.key == self.keys['right']:
                self.move_right = True
                self.current_direction = 1
            elif event.key == self.keys['up']:
                if not self.is_jumping:
                    self.is_jumping = True
                    self.is_walking = False
                    self.jump_velocity = JUMP_SPEED
            elif event.key == self.keys['down']:
                if self.is_jumping and not self.is_dive_kicking:
                    self.is_dive_kicking = True

        elif event.type == SDL_KEYUP:
            if event.key == self.keys['left']:
                self.move_left = False
            elif event.key == self.keys['right']:
                self.move_right = False

    def update(self, dt):
        # ❗️ [수정] 죽었을 때의 업데이트 로직
        if self.is_dead:
            # 죽는 애니메이션 재생
            dead_fps = self.frames.get('dead_fps', 10)
            num_dead_frames = len(self.frames.get('dead', []))
            if num_dead_frames > 0:
                # 마지막 프레임에서 멈추도록 설정
                self.dead_frame = min(self.dead_frame + dead_fps * dt, num_dead_frames - 1)
            return  # 죽었으면 아래 이동 로직은 실행하지 않음

        # --- 살아있을 때의 이동 로직 (기존 코드와 동일) ---
        dx = 0
        if not self.is_jumping:
            if self.move_left:
                dx -= SPEED * dt
                self.is_walking = True
            elif self.move_right:
                dx += SPEED * dt
                self.is_walking = True
            else:
                self.is_walking = False
        else:
            current_speed = SPEED
            if self.is_dive_kicking:
                current_speed = SPEED / 2

            if self.move_left: dx -= current_speed * dt
            if self.move_right: dx += current_speed * dt

        self.x += dx

        if self.is_jumping:
            if self.is_dive_kicking:
                self.jump_velocity = -self.divekick_speed
                self.y += self.jump_velocity * dt
            else:
                self.y += self.jump_velocity * dt
                self.jump_velocity -= GRAVITY * dt

            if self.y <= CHARACTER_GROUND_Y:
                self.y = CHARACTER_GROUND_Y
                self.is_jumping = False
                self.is_dive_kicking = False
                self.jump_velocity = 0.0
                if not self.move_left and not self.move_right:
                    self.is_walking = False

        base_h = self.assets['stand'].h * 2
        base_w = self.assets['stand'].w * 2
        if self.x < base_w // 2: self.x = base_w // 2
        if self.x > CANVAS_W - base_w // 2: self.x = CANVAS_W - base_w // 2
        if self.y > CANVAS_H - base_h // 2: self.y = CANVAS_H - base_h // 2

        if self.is_walking:
            walk_fps = self.frames.get('walk_fps', 10)
            num_walk_frames = len(self.frames.get('walk', []))
            if num_walk_frames > 0:
                self.walk_frame = (self.walk_frame + walk_fps * dt) % num_walk_frames

    def get_hitbox(self):
        # ❗️ [추가] 죽었으면 히트박스 없음 (더 이상 맞지 않음)
        if self.is_dead:
            return (0, 0, 0, 0)

        # (기존 히트박스 계산 로직)
        FIXED_W = 80
        FIXED_H = 150
        draw_w = FIXED_W
        draw_h = FIXED_H
        if self.is_dive_kicking:
            draw_w = int(draw_w * 1.8)

        left = self.x - draw_w / 2
        bottom = self.y - draw_h / 2
        right = self.x + draw_w / 2
        top = self.y + draw_h / 2
        return (left, bottom, right, top)

    def draw(self):
        current_sheet = None
        frame_info = None
        current_sprite_w, current_sprite_h = 0, 0
        draw_x = int(self.x)
        draw_y = int(self.y)

        # ❗️ [수정] 그리기 로직에 '죽음' 상태 추가
        if self.is_dead:
            # 죽는 모션 그리기 설정
            current_sheet = self.assets['dead']
            # 현재 프레임 정보 가져오기
            raw_frame = self.frames['dead'][int(self.dead_frame)]

            # (걷기와 마찬가지로 패딩 처리 필요 시 적용)
            padding = self.rules.get('padding', 0)
            clip_x = raw_frame[0] + padding
            clip_w = max(1, raw_frame[2] - 2 * padding)

            # 그릴 정보 설정
            frame_info = (clip_x, raw_frame[1], clip_w, raw_frame[3])
            current_sprite_w = clip_w
            current_sprite_h = raw_frame[3]

        elif self.is_jumping:
            # ... (기존 점프 그리기 로직) ...
            if self.is_dive_kicking:
                current_sheet = self.assets['divekick']
                current_sprite_w = current_sheet.w
                current_sprite_h = current_sheet.h
            else:
                current_sheet = self.assets['jump']
                if self.jump_velocity > 0:
                    frame_info = self.frames['jump_rise']
                else:
                    frame_info = self.frames['jump_fall']
                current_sprite_w = frame_info[2]
                current_sprite_h = frame_info[3]
        elif self.is_walking:
            # ... (기존 걷기 그리기 로직) ...
            current_sheet = self.assets['walk']
            raw_frame = self.frames['walk'][int(self.walk_frame)]
            padding = self.rules.get('padding', 0)
            clip_x = raw_frame[0] + padding
            clip_w = max(1, raw_frame[2] - 2 * padding)
            frame_info = (clip_x, raw_frame[1], clip_w, raw_frame[3])
            current_sprite_w = clip_w
            current_sprite_h = raw_frame[3]
        else:
            # ... (기존 서기 그리기 로직) ...
            current_sheet = self.assets['stand']
            current_sprite_w = current_sheet.w
            current_sprite_h = current_sheet.h

        # --- 공통 그리기 처리 ---
        draw_w = current_sprite_w * 2
        draw_h = current_sprite_h * 2

        scale = self.rules.get('dive_scale', 1.0)
        if self.is_dive_kicking and scale != 1.0:
            draw_w = int(draw_w * scale)
            draw_h = int(draw_h * scale)

        draw_direction = self.current_direction
        if self.rules.get('jump_flip', False) and self.is_jumping and not self.is_dive_kicking:
            draw_direction = -self.current_direction

        # 최종 그리기
        if frame_info:
            if draw_direction == -1:
                current_sheet.clip_composite_draw(frame_info[0], frame_info[1], frame_info[2], frame_info[3], 0, 'h',
                                                  draw_x, draw_y, draw_w, draw_h)
            else:
                current_sheet.clip_draw(frame_info[0], frame_info[1], frame_info[2], frame_info[3], draw_x, draw_y,
                                        draw_w, draw_h)
        elif current_sheet:
            if draw_direction == -1:
                current_sheet.composite_draw(0, 'h', draw_x, draw_y, draw_w, draw_h)
            else:
                current_sheet.draw(draw_x, draw_y, draw_w, draw_h)

    def take_damage(self, amount):
        # ❗️ [수정] 이미 죽었으면 데미지 안 받음
        if self.is_dead:
            return

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            # ❗️ [추가] HP가 0이 되면 사망 처리
            self.is_dead = True
            # 죽는 순간 모든 행동 정지
            self.move_left = False
            self.move_right = False
            self.is_jumping = False
            self.is_dive_kicking = False
            self.jump_velocity = 0.0
            # 바닥으로 위치 보정 (공중에서 죽었을 경우)
            self.y = CHARACTER_GROUND_Y