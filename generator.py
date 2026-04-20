import anthropic
import json
import os
import random

TOPICS = ["Java", "Spring","자료구조", "알고리즘", "시스템 설계" , "Database", "운영체제", "네트워크", "WEB"]

USED_TOPICS_FILE = os.path.join(os.path.dirname(__file__), "used_topics.json")

PROMPT_TEMPLATE = """당신은 개발 지식을 쉽고 명확하게 설명하는 시니어 개발자입니다.
오늘의 주제: {topics}

위 주제들에서 골고루 선택하여, 개발자라면 알아두면 좋은 핵심 지식 3개를 공유해 주세요.
{used_section}
각 항목은 반드시 아래 JSON 배열 형식으로만 응답하세요 (다른 텍스트 없이):
[
  {{
    "topic": "주제",
    "title": "지식 제목",
    "summary": "해당 개념을 1-2문장으로 핵심만 요약",
    "body": "해당 지식을 설명하는 본문 (개념, 동작 원리, 실무에서 어떻게 쓰이는지 등을 5-8문장으로 설명)",
    "questions": ["더 알아보면 좋을 질문 1", "더 알아보면 좋을 질문 2"],
    "keywords": ["연관 키워드 1", "연관 키워드 2", "연관 키워드 3"],
    "difficulty": "초급|중급|고급"
  }}
]

조건:
- 3개 항목 모두 서로 다른 개념이어야 함
- questions는 답변 없이 질문만, 독자가 스스로 찾아보도록 유도
- keywords는 해당 개념과 연관된 기술/용어로 구성
- 면접용이 아닌, 실제로 이 개념을 이해하고 활용할 수 있도록 설명
- 취업 준비생, 주니어 개발자가 읽기 좋은 수준으로
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
