from logging import INFO
import time
import hydra
from loguru import logger

from common.logging_intercepter import setup_loki_logging

from common.app_config import AppConfig


class UselessComDataImport:
    """Useless.com data import."""

    def __init__(self, cfg: AppConfig):
        """
        Constructor.

        Args:
            cfg (AppConfig): The application config.
        """

        self.__cfg = cfg

    @property
    def cfg(self) -> AppConfig:
        """Get the application config."""
        return self.__cfg

    def run(self):
        """Run the data import."""

        logger.info("Running the data import.")


if __name__ == "__main__":
    """Example of how to use the hydra config."""

    @hydra.main(version_base=None, config_path="conf", config_name="local_config")
    def main(cfg: AppConfig) -> None:
        """
        Main function.

        Args:
            cfg (AppConfig): The application config.

        Returns:
            None
        """

        # Setup Loki integration with Loguru
        setup_loki_logging(INFO)

        # Log the config
        logger.info(f"MongoDB Host: {cfg.mongodb.host}")
        logger.info(f"SQLSever Host: {cfg.mssql.host}")
        logger.info(f"Useless Host: {cfg.useless.host}")
        logger.info(f"YAUA Host: {cfg.yaua.host}")

        # Run the data import
        UselessComDataImport(cfg).run()

    main()
