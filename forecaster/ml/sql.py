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
        where created_at::date <= '{date_to}'::date
        order by created_at asc
    """
