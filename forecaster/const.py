import enum


UAH_ISO_4217 = 980

USD_ISO_4217 = 840

MINUTE = 60

SECOND = 1

HOUR = 60 * 60

REDIS_DEFAULT_TTL_FOR_CACHE = MINUTE * 5

ACTUAL_CURRENCY_REDIS_KEY = 'monobank_actual_currency'

RESPONSE_STATUS_CODE_TOO_MANY_REQUESTS = 429


class CurrencyDymanicPeriod(enum.Enum):
    WEEK = 'Тиждень'
    MONTH = 'Місяць'
    YEAR = 'Рік'
    LAST_5_YEARS = '5 років'
