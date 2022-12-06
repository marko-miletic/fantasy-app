def date_format_changer(date: str, separator: str, format_separator: str) -> str:
    date_list = date.split(separator)
    return format_separator.join(reversed(date_list))
