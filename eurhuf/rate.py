import json
import datetime as dt

class RateHistory:
    def __init__(self, filename : str = "rates.json"):
        with open(filename, "r") as file:
            self.rates = json.load(file)
        first, last = self._get_first_last_date()
        self.first_date = RateHistory.parse_date(first)
        self.last_date = RateHistory.parse_date(last)

    @staticmethod
    def parse_date(date_str: str) -> dt.date:
        return dt.datetime.strptime(date_str, "%Y-%m-%d").date()
        
    def get_rate_on(self, date: dt.date) -> float:
        if date < self.first_date:
            raise KeyError
        if date > self.last_date:
            raise KeyError
        if str(date) in self.rates.keys():
            return self.rates[str(date)]
        return self.get_rate_on(date - dt.timedelta(days=1))
        
    def _get_first_last_date(self) -> tuple[str, str]:
        all_dates = list(self.rates.keys())
        return all_dates[0], all_dates[-1]
    