import calendar
from typing import Dict
from datetime import datetime, date, timedelta

def format_date(raw_date):
    target_date = None
    try:
        target_date = datetime.strptime(raw_date, '%Y-%m-%d')
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        return output_dates(start_of_day, end_of_day)
    except ValueError:
        pass
    return target_date

def amazon_date_parser(rawDate: str, options: Dict = None):
    rawDate = rawDate if rawDate else ''
    date = None
    # datetime.fromisoformat(rawDate)
    eventDate = {}
    if "-" in rawDate:
        res = rawDate.split("-")
        if len(res) == 3:
            date = format_date(rawDate)
            if date:
                return date
    else:
        if "2" in rawDate:
            res = [rawDate]
        else:
            raise Exception("Invalid date")
    meteo_seasons_north_hemisphere = {
        'SP': {
            'startDate': [3, 1],   # 1st of March
            'endDate': [5, 0]      # 31st of May
        },
        'SU': {
            'startDate': [6, 1],   # 1st of June
            'endDate': [8, 0]      # 31st of August
        },
        'FA': {
            'startDate': [9, 1],   # 1st of September
            'endDate': [11, 0]     # 30th of November
        },
        'WI': {
            'startDate': [12, 1],  # 1st of December
            'endDate': [2, 0]      # end of February (28th or 29th)
        }
    }
    if options is None:
        options = {'seasons': meteo_seasons_north_hemisphere}
    else:
        if 'seasonType' not in options:
            options['seasonType'] = 'METEO'
        if 'hemisphere' not in options:
            options['hemisphere'] = 'N'
        if 'seasons' not in options:
            options['seasons'] = meteo_seasons_north_hemisphere
            if options['hemisphere'] == 'S':
                options['seasons'] = south_hemisphere_translation(meteo_seasons_north_hemisphere)
    if date is None:
        if len(res) == 2 and (res[1] == 'SP' or res[1] == 'SU' or res[1] == 'FA' or res[1] == 'WI'):
            season = res[1]
            eventDate['startDate'] = datetime(year=int(res[0]), month=options['seasons'][season]['startDate'][0], day=options['seasons'][season]['startDate'][1], hour=0, minute=0, second=0)
            month = options['seasons'][season]['endDate'][0]
            first_day = datetime.strptime(f"{res[0]}-{month}", '%Y-%m')
            # get the last day of the month for the current datetime object
            last_day = calendar.monthrange(first_day.year, first_day.month)[1]
            # get the last day of the month
            eventDate['endDate'] = datetime(year=int(res[0]), month=month, day=last_day, hour=23, minute=59, second=59)
            return eventDate
        if len(res) == 2 and 'W' in res[1]:
            week_num = int(res[1][1:])
            first_day = f"{res[0]}-{res[1]}-1"
             # -0 means sunday -1 is monday
            last_day = f"{res[0]}-{res[1]}-0"
            first_day = datetime.strptime(first_day, "%Y-W%W-%w")
            last_day = datetime.strptime(last_day, "%Y-W%W-%w")
            # first_day = get_first_day_of_week(res[0], week_num)
            # seven_days_in_minutes = 10079  # six days and 23 hours
            # last_day = first_day + timedelta(minutes=seven_days_in_minutes)
            last_day = last_day.replace(hour=23, minute=59, second=59, microsecond=999999)
            return output_dates(first_day, last_day)
        if len(res) == 2 and 'Q' in res[1]:
            quarter = int(res[1][1:])
            startMonth = ((12 / 4) * quarter) - 3
            endMonth = startMonth + 2
            eventDate['startDate'] = datetime(int(res[0]), startMonth, 1)
            eventDate['endDate'] = datetime(int(res[0]), endMonth + 1, 0, 23, 59, 59, 999)
            return eventDate
        if len(res) == 2:
            date_str = f"{res[0]}-{res[1]}"
            first_day = datetime.strptime(date_str, '%Y-%m')
            # get the last day of the month for the current datetime object
            last_day = calendar.monthrange(first_day.year, first_day.month)[1]
            # create a new datetime object with the last day of the month
            last_day_datetime = datetime(year=first_day.year, month=first_day.month, day=last_day, hour=23, minute=59, second=59, microsecond=999999)
            return output_dates(first_day, last_day_datetime)
        if len(res) == 3 and 'XX' in res[1] and 'XX' in res[2]:
            firstDay = datetime(int(res[0]), 1, 1)
            lastDay = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
            return output_dates(firstDay, lastDay)
        if len(res) == 3 and 'XX' in res[2]:
            firstDay = datetime(int(res[0]), int(res[1]), 1)
            lastDay = datetime(int(res[0]), int(res[1]), 12)
            return output_dates(firstDay, lastDay)
        if len(res) == 3 and 'WE' in res:
            return get_weekend_data(res)
        if len(res) == 1 and 'X' in res[0]:
            partialYear = int(res[0][:3]) * 10
            firstDay = datetime(partialYear, 1, 1)
            lastDay = datetime(partialYear + 10, 1, 1) - timedelta(microseconds=1)
            return output_dates(firstDay, lastDay)
        if len(res) == 1:
            firstDay = datetime(int(res[0]), 1, 1)
            lastDay = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
            return output_dates(firstDay, lastDay)
        if rawDate == 'PRESENT_REF':
            now = datetime.now()
            return {
                'startDate': now,
                'endDate': now
            }
        firstDay = datetime(int(res[0]), 1, 1)
        lastDay = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
        return output_dates(firstDay, lastDay)

def get_last_day_of_year(year):
    if year:
        current_year = year
    else:
        # get the current year
        current_year = datetime.now().year
    # get the datetime for the last month of the year
    last_month = datetime(current_year, 12, 1)
    # get the datetime for the last day of the last month
    last_day = last_month + timedelta(days=31)
    # get the datetime for the last hour of the last day of the last month
    return  datetime(last_day.year, last_day.month, last_day.day, 23, 59, 59)


def get_weekend_data(res):
    week_num = int(res[1][1:])
    first_day = f"{res[0]}-{res[1]}-6"
    # -6 means saturday -0 is sunday
    last_day = f"{res[0]}-{res[1]}-0"
    first_day = datetime.strptime(first_day, "%Y-W%W-%w")
    last_day = datetime.strptime(last_day, "%Y-W%W-%w")
    last_day = last_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    return output_dates(first_day, last_day)

def get_first_day_of_week(year, week):
    year = int(year)
    week_number = int(week)
    # create a datetime object for the first day of the given year
    date = datetime(year, 1, 1)

    # calculate the number of days to add to get to the first day of the given week
    days_to_add = (week_number - 1) * 7

    # add the number of days to the date to get the first day of the given week
    date += timedelta(days=days_to_add)

    # return the datetime object for the first day of the week
    return date
def south_hemisphere_translation(meteo_seasons_north_hemisphere):
    return {
        'SP': meteo_seasons_north_hemisphere['FA'],
        'SU': meteo_seasons_north_hemisphere['WI'],
        'FA': meteo_seasons_north_hemisphere['SP'],
        'WI': meteo_seasons_north_hemisphere['SU'],
    }

def output_dates(start, end):
    return {
        'startDate': start,
        'endDate': end,
    }


