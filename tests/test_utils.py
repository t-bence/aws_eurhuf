import datetime as dt
from eurhuf.rate import RateHistory

def test_date_parsing():
    assert dt.date(2024, 10, 30) == RateHistory.parse_date("2024-10-30")
    
def test_get_rate_on_success():
    date = dt.date(2024, 10, 1)
    history = RateHistory()

    assert 397.29 == history.get_rate_on(date)

def test_first_last_date():
    history = RateHistory()

    first, last = history._get_first_last_date()
    
    assert "2021-01-04" == first
    assert "2024-10-01" == last

def test_prev_rate_used_for_weekend():
    """This method tests that if we are requesting the date for a Sunday,
    we will get the rate for the previous Friday, as rates are not 
    updated on weekends."""

    history = RateHistory()
    
    date = dt.date(2024, 9, 29)
    assert 396.85 == history.get_rate_on(date)