from typing import Tuple, Any, Optional

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data.config import load_config, LOCALES_DIR
from utils.db_api import db_commands


async def get_lang(user_id):
    user = await db_commands.select_user(telegram_id=user_id)
    if user:
        return user.get("language")


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(load_config().tg_bot.I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
