# character.py

from pico2d import *
# 상수는 constants.py에서 가져옴
from constants import *


class Character:
    def __init__(self, x, direction, keys, assets, frames, rules):
        self.x, self.y = x, CHARACTER_GROUND_Y
        self.current_direction = direction
        self.move_left = False
        self.move_right = False
        self.is_jumping = False
        self.is_dive_kicking = False
        self.jump_velocity = 0.0
        self.is_walking = False
        self.walk_frame = 0.0
        self.keys = keys
        self.assets = assets
        self.frames = frames
        self.rules = rules
        self.divekick_speed = self.rules.get('dive_speed', 700.0)

        # HP 변수
        self.hp = 100

    def handle_event(self, event):
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
            if self.move_left: dx -= SPEED * dt
            if self.move_right: dx += SPEED * dt
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

    # --- ❗️ 절대 크기로 고정된 히트박스 ---
    def get_hitbox(self):
        # 1. 기본 히트박스 크기 (평소 크기)
        FIXED_W = 80
        FIXED_H = 150

        draw_w = FIXED_W
        draw_h = FIXED_H

        # 2. 다이브킥 상태일 때 크기 조절
        if self.is_dive_kicking:
            # ❗️ [수정] 가로(너비)를 1.5배, 2.0배 등으로 늘려주세요.
            # (예: 1.8배로 가로만 길어지게 설정)
            draw_w = int(draw_w * 1.8)

            # 세로(높이)는 그대로 두거나, 필요하면 조절하세요.
            # draw_h = int(draw_h * 1.0)

        # 3. 좌표 계산 (수정 X)
        left = self.x - draw_w / 2
        bottom = self.y - draw_h / 2
        right = self.x + draw_w / 2
        top = self.y + draw_h / 2

        return (left, bottom, right, top)

    def draw(self):
        current_sheet = None
        frame_info = None
        # draw 함수는 그림을 그려야 하므로 스프라이트 정보가 필요합니다 (히트박스와 별개)
        current_sprite_w, current_sprite_h = 0, 0
        draw_x = int(self.x)
        draw_y = int(self.y)

        if self.is_jumping:
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
            current_sheet = self.assets['walk']
            raw_frame = self.frames['walk'][int(self.walk_frame)]
            padding = self.rules.get('padding', 0)
            clip_x = raw_frame[0] + padding
            clip_w = max(1, raw_frame[2] - 2 * padding)
            frame_info = (clip_x, raw_frame[1], clip_w, raw_frame[3])
            current_sprite_w = clip_w
            current_sprite_h = raw_frame[3]
        else:
            current_sheet = self.assets['stand']
            current_sprite_w = current_sheet.w
            current_sprite_h = current_sheet.h

        draw_w = current_sprite_w * 2
        draw_h = current_sprite_h * 2

        scale = self.rules.get('dive_scale', 1.0)
        if self.is_dive_kicking and scale != 1.0:
            draw_w = int(draw_w * scale)
            draw_h = int(draw_h * scale)

        draw_direction = self.current_direction

        if self.rules.get('jump_flip', False) and self.is_jumping and not self.is_dive_kicking:
            draw_direction = -self.current_direction

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
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0