#!/usr/bin/env python

def bytestring_to_unicode(text):
    if isinstance(text, bytes):
        return text.decode('utf-8')
    return text

def format_text(text):
    return ' '.join(
        [
            bytestring_to_unicode(s[0]).upper() 
            + bytestring_to_unicode(s[1:]).lower() 
            for s in text.split()
        ]
    )

def validate_date(date):
    elements = date.split('-')
    valid_year = 1800 < int(elements[0]) < 2200
    valid_month = 0 < int(elements[1]) < 13
    valid_day = 0 < int(elements[2]) < 32

    if not valid_year or not valid_month or not valid_day:
        raise ValueError(f'{date} is not a proper date.')
    return date