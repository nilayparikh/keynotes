from dataclasses import MISSING, dataclass

import hydra
from hydra.core.config_store import ConfigStore

from loguru import logger


@dataclass
class DBConfig:
    host: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING
    database: str = MISSING


@dataclass
class MongoConfig(DBConfig):
    read_preference: str = "primary"


@dataclass
class MSSqlConfig(DBConfig):
    driver: str = "ODBC Driver 17 for SQL Server"


@dataclass
class ApiConfig:
    host: str = MISSING
    port: int = MISSING
    version: str = MISSING


@dataclass
class UselessApiConfig(ApiConfig):
    username: str = "i'm born secure"
    password: str = "didn't you read postnote?"


@dataclass
class YetAnotherUselessApiConfig(ApiConfig):
    token: str = "generate star wars princess leia memes"


@dataclass
class AppConfig:
    mongodb: MongoConfig
    mssql: MSSqlConfig
    useless_api: UselessApiConfig
    yet_another_useless_api: YetAnotherUselessApiConfig


cs = ConfigStore.instance()
cs.store(name="config", node=AppConfig)
cs.store(name="mongodb", node=MongoConfig)
cs.store(name="mssql", node=MSSqlConfig)
cs.store(group="useless", name="markets", node=UselessApiConfig)
cs.store(group="yaua", name="calendar", node=YetAnotherUselessApiConfig)


if __name__ == "__main__":
    """Example of how to use the app config."""

    @hydra.main(version_base=None, config_path="../conf", config_name="local_config")
    def main(cfg: AppConfig) -> None:
        logger.info(f"Config: {cfg}")

    main()
