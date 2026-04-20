# TechNote Daily

매일 오전 9시, GitHub Actions가 Claude AI를 호출해 개발 지식 3개를 Mattermost 채널에 자동 발송하는 서비스입니다.

면접 준비용이 아닌, 개발자라면 알아두면 좋은 개념을 쉽고 명확하게 공유하는 것을 목표로 합니다.
이미 다룬 개념은 `used_topics.json`에 누적 관리되어 매번 새로운 주제가 제공됩니다.

**지원 주제:** Java, Spring, 자료구조, 알고리즘, 시스템 설계, Database, 운영체제, 네트워크, WEB

---

## 카드 구성

각 지식 카드는 아래 항목으로 구성됩니다.

| 항목 | 설명 |
|------|------|
| 제목 | 해당 지식의 핵심 개념 제목 |
| 난이도 | 초급 / 중급 / 고급 |
| 요약 | 1-2문장 핵심 요약 |
| 본문 | 개념, 동작 원리, 실무 활용 등 상세 설명 |
| 더 알아보기 | 스스로 찾아볼 심화 질문 2개 |
| 연관 키워드 | 관련 기술/용어 키워드 |

---

## 프로젝트 구조

```
technote/
├── main.py           # 진입점
├── generator.py      # Claude API 호출, 중복 주제 관리
├── printer.py        # Mattermost 메시지 포맷
├── api.py            # Mattermost webhook 전송
├── used_topics.json  # 누적 주제 히스토리 (자동 생성)
└── requirements.txt
```

---

## 로컬 실행

### 환경변수 설정

`.env` 파일을 생성하고 아래 값을 채웁니다.

```env
ANTHROPIC_API_KEY=sk-ant-...
MATTERMOST_WEBHOOK_URL=https://...
```

### 의존성 설치

```bash
pip install -r requirements.txt
```

### 즉시 실행

```bash
python main.py --now
```

---

## GitHub Actions 자동화

`main` 브랜치에 아래 Secrets을 등록하면 매일 오전 9시(KST)에 자동 실행됩니다.

| Secret | 설명 |
|--------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `MATTERMOST_WEBHOOK_URL` | Mattermost Incoming Webhook URL |

실행 후 변경된 `used_topics.json`은 자동으로 커밋되어 히스토리가 유지됩니다.
