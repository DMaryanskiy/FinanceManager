from dataclasses import asdict

def get_value_currency(object: object, currency: str) -> list[str]:
    """
    Function to get a list with sequent pairs "amount, currency, amount, currency...".
    Args:
        object: class instance (Budget and Expense in this case).
        currency: curreny code as string.
    """
    result = []
    for _, value in asdict(object).items():
        result += [value, currency]
    
    return result
