import anthropic
import json
import os
import random

TOPICS = ["Java", "Spring", "시스템 설계", "Database", "OS", "Network"]

USED_TOPICS_FILE = os.path.join(os.path.dirname(__file__), "used_topics.json")

PROMPT_TEMPLATE = """당신은 시니어 개발자이자 기술 면접관입니다.
오늘의 주제: {topics}

위 주제들에서 골고루 선택하여, 기술 면접이나 실제 개발에서 중요한 지식 3개를 만들어 주세요.
{used_section}
각 항목은 반드시 아래 JSON 배열 형식으로만 응답하세요 (다른 텍스트 없이):
[
  {{
    "topic": "주제",
    "title": "핵심 개념 제목",
    "summary": "2-3문장으로 핵심 내용 요약",
    "detail": "실무/면접 관점에서 알아야 할 상세 설명 (4-6문장)",
    "interview_tip": "면접에서 자주 나오는 질문 또는 핵심 포인트 1가지",
    "difficulty": "초급|중급|고급"
  }}
]

조건:
- 3개 항목 모두 서로 다른 개념이어야 함
- 실제 면접이나 실무에서 자주 나오는 중요한 내용 위주로
- 수준은 취업 준비생, 주니어 개발자 수준으로 해줘
- 한국어로 작성
"""


def _load_used_topics() -> dict[str, list[str]]:
    if not os.path.exists(USED_TOPICS_FILE):
        return {}
    with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_used_topics(used: dict[str, list[str]]) -> None:
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def _append_notes_to_used(notes: list[dict], used: dict[str, list[str]]) -> None:
    for note in notes:
        topic = note.get("topic", "")
        title = note.get("title", "")
        if topic and title:
            used.setdefault(topic, [])
            if title not in used[topic]:
                used[topic].append(title)


def _build_used_section(used: dict[str, list[str]]) -> str:
    if not used:
        return ""
    lines = ["이미 다룬 개념 목록 (중복 금지):"]
    for topic, titles in used.items():
        if titles:
            lines.append(f"- {topic}: {', '.join(titles)}")
    lines.append("")
    return "\n".join(lines) + "\n"


def generate_daily_notes() -> list[dict]:
    client = anthropic.Anthropic()

    used = _load_used_topics()

    selected = random.sample(TOPICS, k=min(4, len(TOPICS)))
    remaining = [t for t in TOPICS if t not in selected]
    topics_str = ", ".join(selected + remaining)

    used_section = _build_used_section(used)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        temperature=1.0,
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(topics=topics_str, used_section=used_section),
            }
        ],
    )

    raw = message.content[0].text.strip()

    # JSON 파싱 — 응답에 마크다운 코드블록이 포함될 경우 제거
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    text = raw.strip()
    try:
        notes = json.loads(text)
    except json.JSONDecodeError:
        # 응답이 잘린 경우 완성된 항목만 추출
        last_brace = text.rfind("},")
        if last_brace == -1:
            last_brace = text.rfind("}")
        if last_brace != -1:
            truncated = text[: last_brace + 1] + "\n]"
            notes = json.loads(truncated)
        else:
            raise

    _append_notes_to_used(notes, used)
    _save_used_topics(used)

    return notes
