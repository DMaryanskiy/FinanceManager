class CurrencySingleton(object):
    """ Singleton to store currency code and transmit it between other modules. """
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CurrencySingleton, cls).__new__(cls)
        return cls.instance