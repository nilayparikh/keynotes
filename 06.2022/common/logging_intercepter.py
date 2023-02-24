from itertools import chain
import logging

from logging_loki import LokiHandler

from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercept Python logging messages and forward them to Loguru."""

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(level: int = logging.DEBUG, modules: list = []):
    """Setup logging configuration."""

    logging.basicConfig(handlers=[InterceptHandler()], level=level)

    # Intercept all messages from the modules in the list
    for logger_name in chain(("",), modules):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def setup_loki_logging(level: int = logging.DEBUG):
    """Setup logging configuration."""

    logger.add(
        sink=LokiHandler(
            url="http://localhost:3100/loki/api/v1/push",
            tags={"application": "D02.S01.Nilay.KeyNoteDemo2022.05"},
            version="1",
        ),
        level=level,
    )

    logger.info("Logging to Loki is setup successfully.")


if __name__ == "__main__":
    """Example of how to use the logging intercepter."""

    # TODO: Add example of how to use the logging intercepter.
    # setup_logging()
    pass
else:
    """Setup logging for the rest of the application."""

    # setup_logging(logging.INFO)
    # setup_loki_logging(logging.INFO)
    pass
