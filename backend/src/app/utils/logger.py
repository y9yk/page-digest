import datetime
import logging
import logging.handlers
import re
import sys

import pytz
from pythonjsonlogger import jsonlogger

from src.app.common.config import settings

LOG_FORMAT_PATTERN = "trace_id=%(trace_id)s %(asctime)s %(levelname)-7s %(message)s"


def get_root_logger() -> logging.Logger:
    # create root logger
    root_logger = logging.getLogger(settings.PROJECT_NAME)
    root_logger.setLevel(
        logging.DEBUG if settings.DEBUG else logging.INFO,
    )

    # formatter
    formatter = Formatter(
        "%(level)%(asctime)%(message)%(module)",
        datefmt="%Y-%m-%d %H:%M:%S,%f",
    )
    formatter.json_ensure_ascii = False

    # handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)

    # register handler
    root_logger.addHandler(console_handler)

    #
    return root_logger


def get_logger(name: str) -> logging.Logger:
    # create logger
    logger = logging.getLogger()
    logger.setLevel(
        logging.DEBUG if settings.DEBUG else logging.INFO,
    )

    # formatter
    formatter = Formatter(
        "%(level)%(asctime)%(message)%(module)",
        datefmt="%Y-%m-%d %H:%M:%S,%f",
    )
    formatter.json_ensure_ascii = False

    # handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)

    # register handler
    logger.addHandler(console_handler)

    #
    return logger


class Formatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(Formatter, self).add_fields(log_record, record, message_dict)
        log_status = {"level": record.levelname}
        log_record.update(log_status)

    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        return dt.astimezone(pytz.timezone("Asia/Seoul"))

    def formatTime(self, record, datefmt=None):  # noqa: N802
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()

        return s


class ColorCodes:
    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"


class ColorizedArgsFormatter(logging.Formatter):
    arg_colors = [ColorCodes.purple, ColorCodes.light_blue]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.grey,
        logging.INFO: ColorCodes.green,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    def __init__(self, fmt: str):
        super().__init__()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = ColorizedArgsFormatter.level_to_color[level]
            _format = fmt
            for fld in ColorizedArgsFormatter.level_fields:
                search = "(%\(" + fld + "\).*?s)"
                _format = re.sub(search, f"{color}\\1{ColorCodes.reset}", _format)
            formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        msg = record.msg
        msg = msg.replace("{", "_{{")
        msg = msg.replace("}", "_}}")
        placeholder_count = 0
        # add ANSI escape code for next alternating color before each formatting parameter
        # and reset color after it.
        while True:
            if "_{{" not in msg:
                break
            color_index = placeholder_count % len(ColorizedArgsFormatter.arg_colors)
            color = ColorizedArgsFormatter.arg_colors[color_index]
            msg = msg.replace("_{{", color + "{", 1)
            msg = msg.replace("_}}", "}" + ColorCodes.reset, 1)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)

        if not hasattr(record, "trace_id"):
            record.trace_id = "None"
        formatted = formatter.format(record)

        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted


class BraceFormatStyleFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.formatter = logging.Formatter(fmt)

    @staticmethod
    def is_brace_format_style(record: logging.LogRecord):
        if len(record.args) == 0:
            return False

        msg = record.msg
        if "%" in msg:
            return False

        count_of_start_param = msg.count("{")
        count_of_end_param = msg.count("}")

        if count_of_start_param != count_of_end_param:
            return False

        if count_of_start_param != len(record.args):
            return False

        return True

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        record.msg = record.msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        self.rewrite_record(record)

        if not hasattr(record, "trace_id"):
            record.trace_id = "None"
        formatted = self.formatter.format(record)

        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted
