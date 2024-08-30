#!/usr/bin/env python3
"""
This module contains the filter_datum funtion
"""

import re
import os
from typing import List
import logging
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(handler)
    return logger


def get_db():
    """
    get_db
    """
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(host=host, user=user,
                                   password=password, database=database)


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
