class CurrencySingleton(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CurrencySingleton, cls).__new__(cls)
        return cls.instance