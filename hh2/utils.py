def format_salary(salary):
    if salary is None:
        return None

    to = salary.get('to')
    _from = salary.get('from')

    if to is not None and _from is not None:
        return (to + _from) / 2
    if to is not None:
        return to
    if _from is not None:
        return _from
    return None