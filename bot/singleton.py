class CurrencySingleton(object):
    """ Singleton to store currency code and transmit it between other modules. """
    def __new__(cls):
        if not hasattr(cls, "currency"):
            cls.currency = super(CurrencySingleton, cls).__new__(cls)
        return cls.currency
