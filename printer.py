from datetime import date

DIFFICULTY_LABEL = {"초급": "EASY", "중급": "MEDIUM", "고급": "HARD"}
DIFFICULTY_EMOJI = {"초급": "🟢", "중급": "🟡", "고급": "🔴"}
TOPIC_EMOJI = {
    "Java": "☕",
    "Spring": "🌱",
    "시스템 설계": "🏗️",
    "Database": "🗄️",
    "OS": "💻",
    "Network": "🌐",
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
        f"##### 기술 면접 & 개발 지식 3선\n"
        f"---"
    )

def _build_card(index: int, note: dict) -> str:
    topic = note.get("topic", "")
    emoji = TOPIC_EMOJI.get(topic, "📌")
    difficulty = note.get("difficulty", "중급")
    diff_emoji = DIFFICULTY_EMOJI.get(difficulty, "🟡")
    diff_label = DIFFICULTY_LABEL.get(difficulty, difficulty)

    return (
        f"### {emoji} #{index:02d}  {note.get('title', '')}\n"
        f"`{topic}` {diff_emoji} `{diff_label}`\n\n"
        f"{note.get('summary', '')}\n\n"
        f"**상세 설명**\n"
        f"> {note.get('detail', '')}\n\n"
        f"**💡 면접 팁**\n"
        f"> {note.get('interview_tip', '')}\n\n"
        f"---\n \n \n"
    )

def _build_footer() -> str:
    return ""
