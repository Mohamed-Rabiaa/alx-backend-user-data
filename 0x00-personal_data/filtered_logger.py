#!/usr/bin/env python3
"""
This module contains the filter_datum funtion
"""

import re
from typing import List
import logging


PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    filter_datum
    """
    pattern = '|'.join("{}=[^{}]*".format(field, separator)
                       for field in fields)
    return re.sub(pattern, lambda m: "{}={}".format(
        m.group().split('=')[0], redaction), message)


def get_logger() -> logging.Logger:
    """
    get_logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handle.setFormatter(RedactingFormatter())

    logger.addHandler(handler)
    return logger
