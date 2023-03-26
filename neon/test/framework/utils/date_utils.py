from datetime import datetime, timedelta


class DateUtils:

    def get_zoned_date_time(days=0, hours=0):
        """Get zoned timestamp with microseconds

        Args:
            days (int, optional): Day adjustment (below 0 for past date and above 0 for future), Defaults to 0 (current).
            hours (int, optional): Hours Adjustment(below 0 for past date and above 0 for future). Defaults to 0 (current).

        Returns:
            _type_: ex: 2022-01-05T01:12:30.65465Z
        """
        today = datetime.now() + timedelta(days=days, hours=hours)
        zonedDateTime = today.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        return zonedDateTime

    def get_timestamp(days=0, hours=0):
        """Get current timestamp

        Args:
            days (int, optional): Day adjustment (below 0 for past date and above 0 for future), Defaults to 0 (current).
            hours (int, optional): Hours Adjustment(below 0 for past date and above 0 for future). Defaults to 0 (current).

        Returns:
            str: Retruns in the format of %Y%m%d%H%M%S
        """
        today = datetime.now() + timedelta(days=days, hours=hours)
        today = today.strftime("%Y%m%d%H%M%S")
        return today

    def get_unix_timestamp():
        """Returns current Unix timestamp

        Returns:
            int : 10 digit date based unix timestamp example: 1675154443
        """
        today = datetime.now()
        today = datetime.timestamp(today)
        return int(today * 100000)

    def get_date(days=0, format="%Y-%m-%d"):
        """Get date ex: 2022-01-05

        Args:
            days (int, optional): Day adjustment (below 0 for past date and above 0 for future), Defaults to 0.
            format (str, optional): Date Format. Defaults to "%Y-%m-%d".

        Returns:
            Str: Date ex: 2022-01-05
        """
        today = datetime.now() + timedelta(days=days)
        today = today.strftime(format)
        return today

    def get_date_time(days=0, format="%Y-%m-%dT%H:%M:%S.%f"):
        """Get date time ex: 2022-01-05T01:12:30

        Args:
            days (int, optional): Day adjustment (below 0 for past date and above 0 for future), Defaults to 0.
            format (str, optional): Date Format. Defaults to "%Y-%m-%dT%H:%M:%S.%f".

        Returns:
            Str: DateTime ex: 2022-01-05T01:12:30
        """
        today = datetime.now() + timedelta(days=days)
        today = today.strftime(format)
        return today

    def convert_to_custom_date_time_format(input_date_or_time, input_format="%Y%m%d", format_to_convert="%Y-%m-%d", trim_last=None):
        """Converts your current date time string to desired format
        Args:
            input_date_or_time (_type_): _description_
            input_format (str, optional): _description_. Defaults to "%Y%m%d".
            format_to_convert (str, optional): _description_. Defaults to "%Y-%m-%d".
            trim_last (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if trim_last is not None:
            input_date_or_time = f'{input_date_or_time}'[:-trim_last]
        else:
            input_date_or_time = f'{input_date_or_time}'
        date_time = datetime.strptime(input_date_or_time, f"{input_format}")
        format_to_convert = f"{format_to_convert}"
        new_format = f"{format_to_convert}"
        date_time = date_time.strftime(new_format)
        return date_time

    def str_to_date(current_date: str, format="%Y-%m-%d"):
        """Convert string to date object

        Args:
            current_date (str): string value in date format
            format (str, optional): wrequired date format. Defaults to "%Y-%m-%d".

        Returns:
            _type_: date object
        """
        return datetime.strptime(current_date, format)

    def change_date(current_date: str, days=1):
        """Add or Minus current date to given days

        Args:
            current_date (date): current date
            days (int, optional): + or - days. Defaults to 1.

        Returns:
            date : changed date
        """
        return DateUtils.str_to_date(current_date) + timedelta(days=days)
