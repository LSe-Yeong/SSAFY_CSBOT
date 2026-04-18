# TechNote Daily

매일 GitHub Actions가 Claude AI를 호출해 기술 면접 & 개발 지식 2개를 Mattermost 채널에 자동 발송하는 서비스입니다.

이미 다룬 개념은 `used_topics.json`에 누적 관리되어 매번 새로운 주제가 추천됩니다.

**지원 주제:** Java, Spring, 시스템 설계, Database, OS, Network

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

`main` 브랜치에 아래 Secrets을 등록하면 매일 자동 실행됩니다.

| Secret | 설명 |
|--------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `MATTERMOST_WEBHOOK_URL` | Mattermost Incoming Webhook URL |

실행 후 변경된 `used_topics.json`은 자동으로 커밋되어 히스토리가 유지됩니다.
