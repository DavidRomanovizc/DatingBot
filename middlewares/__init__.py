from aiogram import Dispatcher

from data.config import I18N_DOMAIN, LOCALES_DIR
from .agent_support import SupportMiddleware

from .throttling import ThrottlingMiddleware
from .language_middleware import ACLMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SupportMiddleware())
