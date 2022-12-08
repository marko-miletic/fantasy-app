from src.utility.date_operations import date_format_changer


def test_date_format_changer():
    input_date_space = '1 1 1980'
    input_date_comma = '1,1,1980'
    formatted_output = '1980-1-1'

    assert date_format_changer(input_date_space, ' ', '-') == formatted_output and \
           date_format_changer(input_date_comma, ',', '-') == formatted_output
