import inspect
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List

from environs import Env
from yarl import URL

env = Env()
env.read_env()


# The frozen=True arg protects instances of the class from accidental modification
@dataclass(frozen=True)
class DataBaseConfig:
    user: str
    password: str
    host: str
    database: str
    port: str


@dataclass(frozen=True)
class TgBot:
    token: str
    admin_ids: List[int]
    support_ids: List[int]
    timezone: str
    ip: str
    I18N_DOMAIN: str
    moderate_chat: int
    use_redis: bool


@dataclass(frozen=True)
class Miscellaneous:
    secret_key: str
    yandex_api_key: str
    client_id: str
    redirect_url: URL
    yoomoney_key: str
    production: bool


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    db: DataBaseConfig
    misc: Miscellaneous


def search_env() -> Path:
    current_frame = inspect.currentframe()
    frame = current_frame.f_back
    caller_dir = Path(frame.f_code.co_filename).parent.resolve()
    start = caller_dir / ".env"
    return start


def change_env(section: str, value: str):
    dumped_env = env.dump()
    text = ""
    start = search_env()

    with open(start, "w", encoding="utf-8") as file:
        for v in dumped_env:
            if v:
                e = dumped_env[v]
                if v == section:
                    e = value
                text += f"{v}={e}\n"
        file.write(text)


@lru_cache
def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            support_ids=list(map(int, env.list("SUPPORTS"))),
            ip=env.str("IP"),
            timezone=env.str("TIMEZONE"),
            I18N_DOMAIN="dating",
            moderate_chat=env.int("MODERATE_CHAT"),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DataBaseConfig(
            user=env.str("DB_USER"),
            password=env.str("DB_PASS"),
            host=env.str("DB_HOST"),
            database=env.str("DB_NAME"),
            port=env.str("PORT"),
        ),
        misc=Miscellaneous(
            secret_key=env.str("SECRET_KEY"),
            yandex_api_key=env.str("API_KEY"),
            client_id=env.str("CLIENT_ID"),
            redirect_url=env.str("REDIRECT_URI"),
            yoomoney_key=env.str("YOOMONEY_KEY"),
            production=env.bool("PRODUCTION"),
        ),
    )


# TODO: Move to dataclass
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "locales"
