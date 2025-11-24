# effect.py

from pico2d import *


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('16_sunburn_spritesheet.png')

        # 이미지의 전체 크기를 8x8로 나눔 (스프라이트 시트 구조)
        self.frame_width = self.image.w // 8
        self.frame_height = self.image.h // 8

        self.frame = 0
        # 애니메이션 속도 조절 (숫자가 클수록 빠름)
        self.action_speed = 20.0

        # 이펙트가 끝났는지 확인하는 변수
        self.finished = False

    def update(self, dt):
        # 프레임 증가
        self.frame += self.action_speed * dt

        # 첫 번째 줄(0~7번 프레임)만 재생하고 끝냄
        if self.frame >= 8:
            self.finished = True

    def draw(self):
        frame_index = int(self.frame)

        # 이미지가 끝나지 않았다면 그림
        if frame_index < 8:
            # 첫 번째 줄의 해당 프레임만 잘라냄
            self.image.clip_draw(
                frame_index * self.frame_width,  # x 시작점 (계속 오른쪽으로 이동)
                self.image.h - self.frame_height,  # y 시작점 (맨 윗줄)
                self.frame_width,
                self.frame_height,
                self.x,
                self.y,
                150, 150  # ❗️ 그릴 크기 (너무 크면 여기서 100, 100 등으로 줄이세요)
            )