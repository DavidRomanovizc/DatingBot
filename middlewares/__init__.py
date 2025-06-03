from loader import (
    dp,
    scheduler,
)

from .AgentSupport import (
    SupportMiddleware,
)
from .BanCheck import (
    BanMiddleware,
)
from .IsMaintenanceCheck import (
    IsMaintenance,
)
from .LinkCheck import (
    LinkCheckMiddleware,
)
from .Log import (
    LogMiddleware,
)
from .SchedulerWare import (
    SchedulerMiddleware,
)
from .Throttling import (
    ThrottlingMiddleware,
)

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LinkCheckMiddleware())
    dp.middleware.setup(SupportMiddleware())
    dp.middleware.setup(IsMaintenance())
    dp.middleware.setup(SchedulerMiddleware(scheduler))
    dp.middleware.setup(BanMiddleware())
    dp.middleware.setup(LogMiddleware())
