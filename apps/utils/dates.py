from datetime import date, datetime, timedelta
from typing import Union


def get_current_datetime() -> datetime:
    """
    Returns:
        datetime: Aktualna data i czas.
    """
    return datetime.now()


def get_current_date() -> date:
    """
    Returns:
        date: Dzisiejsza data.
    """
    return date.today()


def format_date(date_obj: Union[datetime, date], format_string: str = '%d-%m-%Y') -> str:
    """
    Formatuje obiekt daty lub datetime na ciąg znaków zgodnie z podanym formatem.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime do sformatowania.
        format_string (str): Ciąg formatu do użycia (domyślnie "%d-%m-%Y").

    Returns:
        str: Sformatowany ciąg znaków reprezentujący datę.
    """
    return date_obj.strftime(format_string)


def parse_date(date_string: str, format_string: str = '%d-%m-%Y') -> datetime:
    """
    Zamienia ciąg znaków reprezentujący datę na obiekt datetime, zgodnie z podanym formatem.

    Args:
        date_string (str): Ciąg znaków do zamiany.
        format_string (str): Ciąg formatowania używanego przy parsowaniu (domyślnie "%d-%m-%Y").

    Returns:
        datetime: Przetworzony obiekt datetime.
    """
    return datetime.strptime(date_string, format_string)


def add_days_to_date(date_obj: Union[datetime, date], days: int) -> Union[datetime, date]:
    """
    Dodaje określoną liczbę dni do obiektu daty lub datetime.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.
        days (int): Liczba dni do dodania.

    Returns:
        Union[datetime, date]: Zaktualizowany obiekt daty lub datetime.
    """
    return date_obj + timedelta(days=days)


def subtract_days_from_date(date_obj: Union[datetime, date], days: int) -> Union[datetime, date]:
    """
    Odejmuje określoną liczbę dni od obiektu daty lub datetime.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.
        days (int): Liczba dni do odjęcia.

    Returns:
        Union[datetime, date]: Zaktualizowany obiekt daty lub datetime.
    """
    return date_obj - timedelta(days=days)


def days_between_dates(start_date: date, end_date: date) -> int:
    """
    Oblicza liczbę dni między dwiema datami.

    Args:
        start_date (date): Data początkowa.
        end_date (date): Data końcowa.

    Returns:
        int: Liczba dni między dwiema datami.
    """
    return (end_date - start_date).days


def is_leap_year(year: int) -> bool:
    """
    Określa, czy podany rok jest rokiem przestępnym.

    Args:
        year (int): Rok do sprawdzenia.

    Returns:
        bool: True, jeśli rok jest przestępny, False w przeciwnym wypadku.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def start_of_day(date_obj: Union[datetime, date]) -> datetime:
    """
    Zwraca początek dnia dla podanej daty.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.

    Returns:
        datetime: Obiekt datetime reprezentujący początek dnia.
    """
    return datetime.combine(date_obj, datetime.min.time())


def end_of_day(date_obj: Union[datetime, date]) -> datetime:
    """
    Zwraca koniec dnia dla podanej daty.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.

    Returns:
        datetime: Obiekt datetime reprezentujący koniec dnia.
    """
    return datetime.combine(date_obj, datetime.max.time())


def to_timestamp(date_obj: datetime) -> int:
    """
    Konwertuje obiekt datetime na znacznik czasu Unix (timestamp).

    Args:
        date_obj (datetime): Obiekt datetime do konwersji.

    Returns:
        int: Znacznik czasu Unix.
    """
    return int(date_obj.timestamp())


def from_timestamp(timestamp: int) -> datetime:
    """
    Konwertuje znacznik czasu Unix na obiekt datetime.

    Args:
        timestamp (int): Znacznik czasu Unix do konwersji.

    Returns:
        datetime: Odpowiadający obiekt datetime.
    """
    return datetime.fromtimestamp(timestamp)


def days_ago(days: int) -> date:
    """
    Zwraca datę sprzed określonej liczby dni.

    Args:
        days (int): Liczba dni do odjęcia od dzisiejszej daty.

    Returns:
        date: Obliczona data.
    """
    return date.today() - timedelta(days=days)


def get_weekday(date_obj: Union[datetime, date]) -> int:
    """
    Zwraca dzień tygodnia dla podanej daty.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.

    Returns:
        int: Dzień tygodnia jako liczbę całkowitą, gdzie poniedziałek to 0, a niedziela to 6.
    """
    return date_obj.weekday()


def get_day_and_month_name(date_obj: Union[datetime, date]) -> str:
    """
    Zwraca nazwę dnia tygodnia oraz miesiąca dla podanej daty.

    Args:
        date_obj (Union[datetime, date]): Obiekt daty lub datetime.

    Returns:
        str: Ciąg znaków zawierający nazwę dnia tygodnia i miesiąca.
    """
    return date_obj.strftime('%A, %B')
