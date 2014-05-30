from datetime import datetime
import calendar


def get_epoch():
    utc_date = datetime.timetuple( datetime.utcnow() )
    return calendar.timegm(utc_date)