from aiogram import Dispatcher

from data.config import I18N_DOMAIN, LOCALES_DIR
from .throttling import ThrottlingMiddleware
from .language_middleware import ACLMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware(domain=I18N_DOMAIN, path=LOCALES_DIR))