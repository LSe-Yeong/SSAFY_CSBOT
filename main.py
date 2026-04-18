import os
import sys
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

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

def run_pipeline() -> None:
    logger.info("파이프라인 시작")
    try:
        logger.info("LLM으로 오늘의 기술 노트 생성 중...")
        notes = generate_daily_notes()
        logger.info(f"{len(notes)}개 항목 생성 완료")
        sendApi(format_notes(notes))
        logger.info(f"{len(notes)}개 게시 완료")
    except Exception as e:
        logger.error(f"파이프라인 오류: {e}", exc_info=True)
        raise

def main() -> None:
    if "--now" in sys.argv:
        run_pipeline()
        return

    send_time = os.getenv("SEND_TIME", "23:00")
    hour, minute = map(int, send_time.split(":"))

    scheduler = BlockingScheduler(timezone="Asia/Seoul")
    scheduler.add_job(
        run_pipeline,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_technote",
    )

    logger.info(f"스케줄러 시작 — 매일 {send_time} KST 실행")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("스케줄러 종료")

if __name__ == "__main__":
    main()
