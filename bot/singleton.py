from sqlalchemy.ext.asyncio import AsyncSession


class CurrencySingleton(object):
    """ Singleton to store currency code and transmit it between other modules. """
    def __new__(cls):
        if not hasattr(cls, "currency"):
            cls.currency: str = super(CurrencySingleton, cls).__new__(cls)
        return cls.currency


class SessionSingleton(object):
    def __new__(cls):
        if not hasattr(cls, "session"):
            cls.session: AsyncSession = super(SessionSingleton, cls).__new__(cls)
        return cls.session
