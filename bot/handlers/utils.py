from dataclasses import asdict

def get_value_currency(object: object, currency: str) -> list[str]:
    result = []
    for _, value in asdict(object).items():
        result += [value, currency]
    
    return result
