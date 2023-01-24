import asyncio


class AsyncObj:
    def __init__(self, *args, **kwargs):
        """
        Standard constructor used for arguments pass
        Do not override. Use __ainit__ instead
        """
        self.__stored_args = args, kwargs
        self.async_initialized = False

    async def __ainit__(self, *args, **kwargs):
        """ Async constructor, you should implement this """

    async def __initobj(self):
        """ Crutch used for __await__ after spawning """
        assert not self.async_initialized
        self.async_initialized = True
        # pass the parameters to __ainit__ that passed to __init__
        await self.__ainit__(*self.__stored_args[0],
                             **self.__stored_args[1])
        return self

    def __await__(self):
        return self.__initobj().__await__()

    def __init_subclass__(cls, **kwargs):
        # __ainit__ must be async
        assert asyncio.iscoroutinefunction(cls.__ainit__)

    @property
    def async_state(self):
        if not self.async_initialized:
            return "[initialization pending]"
        return "[initialization done and successful]"
