# poker-web

이 폴더는 웹 프론트엔드와 Flask 백엔드 서버 코드를 포함합니다.

- `index.html` : 웹 프론트엔드(사용자 인터페이스)
- `web_server.py` : Flask 기반 API 서버
- `exact_probability.py` : 정확한 포커 승률 계산 로직 (서버에서 사용)
- `poker.py` : 카드/핸드 평가 로직 (서버에서 사용)

---

## 사용법
1. `py web_server.py`로 서버 실행
2. `index.html` 또는 상위 폴더의 `poker_calculator.html`을 브라우저에서 열기 