from typing import (
    Any,
    Optional,
    Tuple,
)

from aiogram import (
    types,
)
from aiogram.contrib.middlewares.i18n import (
    I18nMiddleware,
)

from data.config import (
    LOCALES_DIR,
    load_config,
)
from utils.db_api import (
    db_commands,
)


async def get_lang(user_id) -> Optional[str]:
    user = await db_commands.select_user(telegram_id=user_id)
    return user.language if user else None


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user_id = types.User.get_current().id
        return await get_lang(user_id) or (await super().get_user_locale(action, args))


def setup_middleware(dp) -> ACLMiddleware:
    i18n = ACLMiddleware(load_config().tg_bot.I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
