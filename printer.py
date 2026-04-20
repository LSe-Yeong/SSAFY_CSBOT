from datetime import date

DIFFICULTY_EMOJI = {"초급": "🟢", "중급": "🟡", "고급": "🔴"}
TOPIC_EMOJI = {
    "Java": "☕",
    "Spring": "🌱",
    "자료구조": "🧱",
    "알고리즘": "⚙️",
    "시스템 설계": "🏗️",
    "Database": "🗄️",
    "운영체제": "💻",
    "네트워크": "🌐",
    "WEB": "🌍",
}

def format_notes(notes: list[dict]) -> str:
    today = date.today().strftime("%Y.%m.%d")
    parts = [_build_header(today)]
    for i, note in enumerate(notes):
        parts.append(_build_card(i + 1, note))
    parts.append(_build_footer())
    return "\n".join(parts)


def _build_header(today: str) -> str:
    return (
        f"## 📚 Daily Tech Notes  |  {today}\n"
        f"##### 오늘의 개발 지식 3선\n"
        f"---"
    )

def _build_card(index: int, note: dict) -> str:
    topic = note.get("topic", "")
    emoji = TOPIC_EMOJI.get(topic, "📌")
    difficulty = note.get("difficulty", "중급")
    diff_emoji = DIFFICULTY_EMOJI.get(difficulty, "🟡")

    return (
        f"### {emoji} #{index:02d}  {note.get('title', '')}\n"
        f"`{topic}` {diff_emoji} `{difficulty}`\n\n"
        f"{note.get('body', '')}\n\n"
        f"---\n \n \n"
    )

def _build_footer() -> str:
    return ""
