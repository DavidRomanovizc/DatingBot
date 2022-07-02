from loader import dp
from .agent_support import SupportMiddleware
from .ban_check import BanMiddleware
from .is_maintenance_check import IsMaintenance
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BanMiddleware())
    # dp.middleware.setup(IsMaintenance())
    dp.middleware.setup(SupportMiddleware())

