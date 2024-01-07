import calendar
from typing import Dict
from datetime import datetime, timedelta
import pytz
from pytz import timezone


def convert_to_utc(naive_dt, timezone_string=""):
    # Default timezone
    if not timezone_string:
        timezone_string = "America/Los_Angeles"

    # Check if the datetime is naive
    if naive_dt.tzinfo is not None and naive_dt.tzinfo.utcoffset(naive_dt) is not None:
        raise ValueError("The provided datetime is not naive. It already has timezone information.")

    try:
        local_tz = timezone(timezone_string)
        local_dt = local_tz.localize(naive_dt)
        # Convert this date to GMT
        return local_dt.astimezone(pytz.utc)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Invalid timezone string: {timezone_string}")


def format_date(raw_date, timezone_string):
    try:
        target_date = datetime.strptime(raw_date, '%Y-%m-%d')
        target_date = convert_to_utc(target_date, timezone_string)
        return get_start_and_end(target_date, target_date)
    except:
        return None


def get_start_and_end(start_day, end_day):
    start_of_day = start_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = end_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    return output_dates(start_of_day, end_of_day)


def convert_to_utc_if_needed(first_day, last_day, timezone_string):
    first_day = convert_to_utc(first_day, timezone_string)
    last_day = convert_to_utc(last_day, timezone_string)
    return output_dates(first_day, last_day)


def amazon_date_parser(raw_date: str, timezone_string: str = None, options: Dict = None):
    raw_date = raw_date if raw_date else ''
    final_date = None
    if "-" in raw_date:
        res = raw_date.split("-")
        if len(res) == 3:
            final_date = format_date(raw_date, timezone_string)
            if final_date:
                return final_date
    else:
        if "2" in raw_date:
            res = [raw_date]
    if final_date is None:
        list_of_seasons = ['SP', 'SU', 'FA', 'WI']
        if len(res) == 2 and (res[1] in list_of_seasons):
            meteo_seasons_north_hemisphere = {
                'SP': {
                    'startDate': [3, 1],  # 1st of March
                    'endDate': [5, 31]  # 31st of May
                },
                'SU': {
                    'startDate': [6, 1],  # 1st of June
                    'endDate': [8, 31]  # 31st of August
                },
                'FA': {
                    'startDate': [9, 1],  # 1st of September
                    'endDate': [11, 30]  # 30th of November
                },
                'WI': {
                    'startDate': [12, 1],  # 1st of December
                    'endDate': [2, 28]  # end of February (28th or 29th)
                }
            }
            return get_season_dates(res, options, meteo_seasons_north_hemisphere, timezone_string)
        if len(res) == 2 and 'W' in res[1]:
            return get_week_dates(res, timezone_string)
        if len(res) == 2 and 'Q' in res[1]:
            return get_quarter_dates(res, timezone_string)
        if len(res) == 2:
            return get_month_dates(res, timezone_string)
        if len(res) == 3 and 'XX' in res[1] and 'XX' in res[2]:
            first_day = datetime(int(res[0]), 1, 1)
            last_day = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
            return convert_to_utc_if_needed(first_day, last_day, timezone_string)
        if len(res) == 3 and 'XX' in res[2]:
            return get_month_dates(res, timezone_string)
        if len(res) == 3 and 'WE' in res:
            return get_weekend_data(res, timezone_string)
        if len(res) == 1 and 'X' in res[0]:
            partial_year = int(res[0][:3]) * 10
            first_day = datetime(partial_year, 1, 1)
            last_day = datetime(partial_year + 10, 1, 1) - timedelta(microseconds=1)
            return convert_to_utc_if_needed(first_day, last_day, timezone_string)
        if len(res) == 1:
            first_day = datetime(int(res[0]), 1, 1)
            last_day = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
            return convert_to_utc_if_needed(first_day, last_day, timezone_string)
        if raw_date == 'PRESENT_REF':
            now = datetime.now()
            return {
                'startDate': now,
                'endDate': now
            }
        first_day = datetime(int(res[0]), 1, 1)
        last_day = datetime(int(res[0]), 12, 31, 23, 59, 59, 999999)
        return output_dates(first_day, last_day)


def get_last_day_of_month(year, month):
    """Returns the last day of the month for a given year and month.

    Args:
        year (int): The year of the month.
        month (int): The month to get the last day for.

    Returns:
        int: The last day of the month.
    """
    return calendar.monthrange(year, month)[1]


def get_month_dates(res, timezone_string):
    """Returns the start and end dates for a given month and timezone.

    Args:
        res (list): A list containing the year and month as strings in the format ["YYYY", "MM"].
        timezone_string (str): A string representing the timezone in which to return the dates.

    Returns:
        tuple: A tuple containing the start and end dates for the month in the given timezone.
    """
    date_str = f"{res[0]}-{res[1]}"
    first_day = datetime.strptime(date_str, '%Y-%m')
    last_day_of_month = get_last_day_of_month(first_day.year, first_day.month)
    last_day = datetime(
        year=first_day.year,
        month=first_day.month,
        day=last_day_of_month,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )
    return convert_to_utc_if_needed(first_day, last_day, timezone_string)


def get_quarter_dates(res, timezone_string):
    """Calculate the start and end dates of the quarter for a given date string in the format 'YYYY-Qx'."""
    try:
        year = res[0]
        quarter_string = res[1]
        quarter_number = int(quarter_string[1])
        if quarter_number < 1 or quarter_number > 4:
            raise ValueError("Invalid quarter number")
        start_month = (quarter_number - 1) * 3 + 1
        end_month = start_month + 2
        start_date = datetime(year, start_month, 1)
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        return convert_to_utc_if_needed(start_date, end_date, timezone_string)
    except (ValueError, AttributeError):
        # Handle cases where the input string is not in the expected format
        # or the quarter number is invalid
        raise ValueError("Invalid date string")


def get_season_dates(res, options, meteo_seasons_north_hemisphere, timezone_string):
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
    season = res[1]
    first_day = datetime(year=int(res[0]), month=options['seasons'][season]['startDate'][0],
                         day=options['seasons'][season]['startDate'][1], hour=0, minute=0,
                         second=0)
    month = options['seasons'][season]['endDate'][0]
    end_date_month = datetime.strptime(f"{res[0]}-{month}", '%Y-%m')
    # get the last day of the month for the current datetime object
    last_day_of_month = get_last_day_of_month(end_date_month.year, end_date_month.month)
    # get the last day of the month
    last_day = datetime(year=int(res[0]), month=month, day=last_day_of_month, hour=23, minute=59, second=59)
    return convert_to_utc_if_needed(first_day, last_day, timezone_string)


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
    return datetime(last_day.year, last_day.month, last_day.day, 23, 59, 59)


def get_week_dates(res: list, timezone: str):
    """
    Given a list (year, week_number), returns the start and end dates of the week in UTC timezone.

    Args:
        res (list): A tuple containing the year and week number.
        timezone (str): A string representing the timezone.

    Returns:
        tuple: A dictionary containing the start and end dates of the week in UTC timezone.
    """

    try:
        year = int(res[0])
        week_number = int(res[1][1:])  # Remove the 'W' prefix

        # Calculate the start date of the week (Monday)
        # Jan 4th is always in the first week according to ISO week date system
        jan4 = datetime(year, 1, 4)
        start_of_week = jan4 + timedelta(weeks=(week_number - 1) - jan4.weekday() / 7)

        end_of_week = start_of_week + timedelta(days=6)
        return get_start_and_end(convert_to_utc(start_of_week, timezone),
                                 convert_to_utc(end_of_week, timezone))
    except ValueError as e:
        raise ValueError("Invalid week number or year") from e

    # Convert the dates to UTC timezone if necessary
    # return convert_to_utc_if_needed(start_date, end_date, timezone_string)


def get_weekend_data(res: list, timezone: str):
    try:
        year = int(res[0])
        week_number = int(res[1][1:])  # Remove the 'W' prefix

        # Calculate the start date of the week (Monday)
        # Jan 4th is always in the first week according to ISO week date system
        jan4 = datetime(year, 1, 4)
        start_of_week = jan4 + timedelta(weeks=(week_number - 1) - jan4.weekday() / 7)

        # Calculate Saturday (start of weekend)
        saturday = start_of_week + timedelta(days=5)

        # Calculate Sunday (end of weekend)
        sunday = start_of_week + timedelta(days=6)
        return get_start_and_end(convert_to_utc(saturday, timezone),
                                 convert_to_utc(sunday, timezone))
    except ValueError as e:
        raise ValueError("Invalid week number or year") from e


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
