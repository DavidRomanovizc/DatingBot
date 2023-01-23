from loader import dp, scheduler
from .SchedulerWare import SchedulerMiddleware
from .AgentSupport import SupportMiddleware
from .BanCheck import BanMiddleware
from .IsMaintenanceCheck import IsMaintenance
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SupportMiddleware())
    dp.middleware.setup(IsMaintenance())
    dp.middleware.setup(SchedulerMiddleware(scheduler))
    dp.middleware.setup(BanMiddleware())
