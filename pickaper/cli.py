
import logging
import argparse

from pickaper import settings

from .runner import start_delivery

logger = logging.getLogger(__name__)


def set_logging(log_level: str | int = logging.INFO) -> None:
    """
        set basic log configuration
        :return: None
    """
    logging.basicConfig(
        format='%(asctime)s(%(name)s)[%(levelname)s]: %(message)s',
        level=log_level,
    )


async def main(args: list[str]) -> None:
    """
        command line entranse; parse cli params and start delivering
        :param args: cli args (like sys.argv)
        :return:
    """
    parser = argparse.ArgumentParser(description='Package delivery emulator')
    parser.add_argument(
        '--cars',
        action='store',
        default=settings.CARS_COUNT,
        type=int,
        help=f'set number of cars; default {settings.CARS_COUNT}',
    )
    parser.add_argument(
        '--log-level',
        action='store',
        default=settings.LOG_LEVEL,
        type=str,
        help=f'set log level; default {settings.LOG_LEVEL}',
    )

    cli_args = parser.parse_args(args)

    set_logging(log_level=cli_args.log_level)
    await start_delivery(cars_count=cli_args.cars)
