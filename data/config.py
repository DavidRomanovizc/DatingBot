from dataclasses import dataclass
from typing import List

from environs import Env


# параметр frozen=True защищает экземпляры класса от случайного изменения
@dataclass(frozen=True)
class DataBaseConfig:
    user: str
    password: str
    host: str
    database: str


@dataclass(frozen=True)
class TgBot:
    token: str
    admin_ids: List[int]
    support_ids: List[int]
    ip: str


@dataclass(frozen=True)
class Miscellaneous:
    secret_key: str
    yandex_api_key: str


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    db: DataBaseConfig
    misc: Miscellaneous


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            support_ids=list(map(int, env.list("SUPPORTS"))),
            ip=env.str("IP"),
        ),
        db=DataBaseConfig(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            secret_key=env.str("SECRET_KEY"),
            yandex_api_key=env.str('API_KEY')
        )
    )
