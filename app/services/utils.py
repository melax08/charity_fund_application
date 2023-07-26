from datetime import datetime


def close_obj(obj) -> None:
    """Makes project or donation closed."""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
