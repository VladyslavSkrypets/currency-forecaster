import datetime


def sql_get_all_currency_data(date_to: datetime.date) -> str:
    if not isinstance(date_to, datetime.date):
        raise ValueError(
            "Passed param \"date_to\" must have \"datetime.date\" type"
        )

    return f"""
        select
            buy,
            sell,
            created_at
        from currency
        where created_at < '{date_to}'::date
    """


def sql_get_currency_data_by_period(
    date_from: datetime.date,
    date_to: datetime.date,
) -> str:
    if (
        (not isinstance(date_from, datetime.date))
        or (not isinstance(date_to, datetime.date))
    ):
        raise ValueError("Passed params must have \"datetime.date\" type")
    
    if date_from > date_to:
        raise ValueError("Param \"date_from\" can not be greater then \"date_to\"")
    
    return f"""
        select
            buy,
            sell,
            created_at
        from currency
        where created_at between '{date_from}'::date and '{date_to}'::date
    """
