import logging
from dotenv import load_dotenv

from generator import generate_daily_notes
from printer import format_notes
from api import sendApi

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("파이프라인 시작")
    notes = generate_daily_notes()
    logger.info(f"{len(notes)}개 항목 생성 완료")
    sendApi(format_notes(notes))
    logger.info(f"{len(notes)}개 게시 완료")

if __name__ == "__main__":
    main()
