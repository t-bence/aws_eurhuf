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
    
    @staticmethod
    def previous_day(day: dt.date) -> dt.date:
        return day - dt.timedelta(days=1)
        
    def get_rate_on(self, date: dt.date) -> float:
        """Get the rate on a specific day.
        If the requested day was on a weekend, we get the rate from a day before (iteratively).

        Parameters
        ----------
        date : dt.date
            The day on which we get the EURHUF rate.

        Returns
        -------
        float
            The EURHUF rate.

        Raises
        ------
        KeyError
            If the requested day is out of the range of the stored data.
        """
        if date < self.first_date:
            raise KeyError
        if date > self.last_date:
            raise KeyError
        if str(date) in self.rates.keys():
            return self.rates[str(date)]
        return self.get_rate_on(RateHistory.previous_day(date))
        
    def _get_first_last_date(self) -> tuple[str, str]:
        all_dates = list(self.rates.keys())
        return all_dates[0], all_dates[-1]
    