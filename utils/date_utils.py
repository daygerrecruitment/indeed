def today_date():
    from datetime import datetime
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d %B %Y')
    return formatted_date

def check_by_date(date_of_post):
    if date_of_post == today_date():
        return True
    return False