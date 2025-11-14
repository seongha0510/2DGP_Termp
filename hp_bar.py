# hp_bar.py

from pico2d import *


class HpBar:
    """
    중앙에 위치하는 통합 HP 바 클래스.
    (설명 생략)
    """

    def __init__(self, x, y, width, height):
        self.x = x  # main.py에서 받은 중심 x
        self.y = y  # main.py에서 받은 중심 y
        self.width = width  # ❗️ main.py에서 받은 너비 (예: 760)

        # --- ❗️ [수정] 원본 이미지 비율 유지 로직 ---
        self.frame_image = load_image('hp_bar.png')
        self.fill_image = load_image('hp_red.png')

        # 원본 이미지의 가로, 세로 크기를 가져옴
        original_w = self.frame_image.w
        original_h = self.frame_image.h

        # 원본의 가로세로 비율 계산 (높이 / 너비)
        aspect_ratio = original_h / original_w

        # main.py에서 넘겨준 height(50)를 무시하고,
        # 너비(self.width)에 맞춰 비율이 유지되는 새 높이를 계산
        self.height = self.width * aspect_ratio
        # --- [수정] 끝 ---

        # 붉은색 막대의 높이 (새로 계산된 self.height 기준)
        self.fill_height = self.height * 0.6

        # 붉은색 막대의 최대 너비 (self.width 기준)
        self.max_fill_width_per_player = self.width * 0.42

        # 중앙 패딩 (self.width 기준)
        self.center_padding = self.width * 0.08

    def draw(self, p1_hp, p2_hp, max_hp=100):
        """P1과 P2의 현재 HP를 기준으로 붉은색 막대와 프레임을 그립니다."""

        # (이 함수는 기존 코드와 동일하므로 수정할 필요 없습니다)

        # --- 1. P1 (왼쪽) HP 그리기 ---
        p1_ratio = max(0, p1_hp / max_hp)
        p1_fill_w = int(self.max_fill_width_per_player * p1_ratio)

        if p1_fill_w > 0:
            fill_right_edge = self.x - self.center_padding
            p1_draw_x = fill_right_edge - (p1_fill_w / 2)
            self.fill_image.draw(p1_draw_x, self.y, p1_fill_w, self.fill_height)

        # --- 2. P2 (오른쪽) HP 그리기 ---
        p2_ratio = max(0, p2_hp / max_hp)
        p2_fill_w = int(self.max_fill_width_per_player * p2_ratio)

        if p2_fill_w > 0:
            fill_left_edge = self.x + self.center_padding
            p2_draw_x = fill_left_edge + (p2_fill_w / 2)
            self.fill_image.draw(p2_draw_x, self.y, p2_fill_w, self.fill_height)

        # --- 3. 프레임 그리기 (항상 맨 위에) ---
        # (self.width와 새로 계산된 self.height를 사용)
        self.frame_image.draw(self.x, self.y, self.width, self.height)