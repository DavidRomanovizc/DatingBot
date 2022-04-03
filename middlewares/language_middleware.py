from aiogram.contrib.middlewares.i18n import I18nMiddleware
from data.config import LOCALES_DIR, I18N_DOMAIN
from typing import Tuple, Any, Optional
from aiogram import types


# Unused
class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
