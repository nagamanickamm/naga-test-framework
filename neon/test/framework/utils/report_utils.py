from getgauge.python import Messages
import os


class ReportUtils:
    level_info = 'info'

    def log(str_message, log_level='debug'):
        str_message = str(str_message)
        log_settings = 'both' if os.getenv('log') is None else os.getenv('log')
        if log_settings == 'report' and log_level == 'info':
            Messages.write_message(str_message)
        elif log_settings == 'console' and log_level == 'debug':
            print(str_message)
        elif log_settings == 'both' and log_level == 'info':
            print(str_message)
            Messages.write_message(str_message)
