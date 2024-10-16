import json
import datetime as dt

def get_rate_on(date: dt.date) -> float:
    with open("rates.json", "r") as file:
        rates = json.load(file)
        
    query_date = str(date)
    if query_date not in rates.keys():
        raise ValueError
    else:
        return rates[query_date]

def get_first_last_date() -> str:
    with open("rates.json", "r") as file:
        rates = json.load(file)
    dates = list(rates.keys())
    return dates[0], dates[-1]

def lambda_handler(event, context):
    if "date" in event["queryStringParameters"].keys():
        date_str = event["queryStringParameters"]["date"]
    else:
        return {"statusCode": 400, "body": "Parameter date is missing"}
    
    try:
        date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return {
            "statusCode": 422,
            "body": "Could not parse date, format must be YYYY-mm-dd"
        }
        
    try:
        rate = get_rate_on(date)
    except ValueError:
        first_date, last_date = get_first_last_date()
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": f"No data found for date {str(date)}",
                "first_date": first_date,
                "last_date": last_date
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

