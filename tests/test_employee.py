from collector import validate_date


def test_date_validation():
    real_date = '12/14/2015'
    false_date = '33/90/2016'
    plain_string = 'test'
    assert validate_date(real_date) == True
    assert validate_date(false_date) == False
    assert validate_date(plain_string) == False
