import json
from eurhuf.rate import RateHistory

def lambda_handler(event, context):
    try:
        date_str = event["queryStringParameters"]["date"]
    except KeyError:
        return {"statusCode": 400, "body": "Parameter date is missing"}
    
    try:
        date = RateHistory.parse_date(date_str)
    except ValueError:
        return {
            "statusCode": 422,
            "body": "Could not parse date, format must be YYYY-mm-dd"
        }
    
    rate_history = RateHistory()
    try:
        rate = rate_history.get_rate_on(date)
    except KeyError:
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
            "statusCode": 400,
            "body": repr(e)
        }
    return {
        "statusCode": 200,
        "body": json.dumps({
            "date": str(date),
            "rate": rate
        })
    }        
