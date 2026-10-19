import argparse
import logging
import signal
import sys
import time
from datetime import datetime, timezone

from pipeline import main, USE_BIGQUERY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("scheduler.log"), logging.StreamHandler()],
)
log = logging.getLogger("scheduler")

running = True


def handle_signal(signum, frame):
    global running
    log.info("Received signal %s, shutting down gracefully", signum)
    running = False


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


def run_once() -> bool:

    start = datetime.now(timezone.utc)
    try:
        main()
        duration = (datetime.now(timezone.utc) - start).total_seconds()
        log.info("Pipeline run completed successfully in %.2fs", duration)
        return True
    except Exception as exc:
        duration = (datetime.now(timezone.utc) - start).total_seconds()
        log.error("Pipeline run failed after %.2fs: %s", duration, exc)
        return False


def run_loop(interval_seconds: int) -> None:
    log.info("Scheduler started (interval=%ss, bigquery=%s)", interval_seconds, USE_BIGQUERY)
    while running:
        run_once()
        if not running:
            break
        log.info("Next run in %ss", interval_seconds)
        time.sleep(interval_seconds)
    log.info("Scheduler stopped")


def main_cli() -> None:
    parser = argparse.ArgumentParser(description="Compass data pipeline scheduler")
    parser.add_argument("--once", action="store_true", help="Run a single pipeline iteration and exit")
    parser.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Interval between runs in seconds (default 3600 = 1 hour)",
    )
    args = parser.parse_args()

    if args.once:
        success = run_once()
        sys.exit(0 if success else 1)
    run_loop(args.interval)


if __name__ == "__main__":
    main_cli()