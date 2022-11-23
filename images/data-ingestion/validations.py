#!/usr/bin/env python


def bytestring_to_unicode(text: str) -> str:
    """
    Checks the entry if it is a bytestring, then decodes to UTF-8.
    Else returns the string back.

    :param text: input text
    :type text: str
    """
    if isinstance(text, bytes):
        return text.decode("utf-8")
    return text


def format_text(text: str) -> str:
    """
    Formats the text given bytestring conversion and upper/lower case correction.
    :param text: text input
    :type text: str
    """
    return " ".join(
        [
            bytestring_to_unicode(s[0]).upper() + bytestring_to_unicode(s[1:]).lower()
            for s in text.split()
        ]
    )


def validate_date(date: str) -> str:
    """
    Validates the given date by splitting the elements,
    and checking the general ranges for a year, month, and day.
    Note that the validation is not complete as it does not consider
    the assignments between months and days.

    :param date: date input
    :type date: str
    """
    elements = date.split("-")
    valid_year = 1800 < int(elements[0]) < 2200
    valid_month = 0 < int(elements[1]) < 13
    valid_day = 0 < int(elements[2]) < 32

    if not valid_year or not valid_month or not valid_day:
        raise ValueError(f"{date} is not a proper date.")
    return date
