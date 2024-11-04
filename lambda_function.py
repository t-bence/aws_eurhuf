import json
from eurhuf.rate import RateHistory
from eurhuf.errors import DateParsingError, MissingParameterError, RateNotFoundError

def parse_date_or_error(date_str):
    if not date_str:
        raise MissingParameterError("Parameter date is missing")
    try:
        return RateHistory.parse_date(date_str)
    except ValueError:
        raise DateParsingError("Could not parse date, format must be YYYY-mm-dd")

def get_rate_or_error(rate_history, date):
    try:
        return rate_history.get_rate_on(date)
    except KeyError:
        raise RateNotFoundError(date)

def lambda_handler(event, context):
    try:
        date_str = event.get("queryStringParameters", {}).get("date")
        date = parse_date_or_error(date_str)

        rate_history = RateHistory()
        rate = get_rate_or_error(rate_history, date)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "date": str(date),
                "rate": rate
            })
        }
    
    except MissingParameterError as e:
        return {"statusCode": 400, "body": str(e)}
    
    except DateParsingError as e:
        return {"statusCode": 422, "body": str(e)}

    except RateNotFoundError:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": f"No data found for date {date_str}",
                "first_date": str(rate_history.first_date),
                "last_date": str(rate_history.last_date)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": repr(e)
            })
        }
