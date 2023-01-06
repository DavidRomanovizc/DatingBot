from loader import dp, scheduler
from .SchedulerWare import SchedulerMiddleware
from .agent_support import SupportMiddleware
from .ban_check import BanMiddleware
from .is_maintenance_check import IsMaintenance
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SupportMiddleware())
    dp.middleware.setup(IsMaintenance())
    dp.middleware.setup(SchedulerMiddleware(scheduler))
    dp.middleware.setup(BanMiddleware())
