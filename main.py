# main.py (새로운 게임 시작점)

import framework
import title_state # 타이틀 화면 모듈 임포트

# 게임 시작 시 title_state(타이틀 화면)부터 시작하도록 프레임워크에 지시
framework.run(title_state)