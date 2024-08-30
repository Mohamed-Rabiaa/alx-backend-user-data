#!/usr/bin/env python3
"""
This module contains the filter_datum funtion
"""

import re
import os
import logging
import mysql.connector
from typing import List


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(host=host, user=user, port=3306,
                                   password=password, database=db_name)


def main() -> None:
    """
    main
    """
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            result = cursor.fetchall()
            logger = get_logger()

            for row in result:
                name, email, phone, ssn, password, ip, \
                    last_login, user_agent = row
                message = (
                    'name={}; email={}; phone={}; ssn={}; password={}; '
                    'ip={}; last_login={}; user_agent={};').format(
                    name, email, phone, ssn, password, ip, last_login,
                        user_agent)
                logger.info(message)

    except mysql.connector.Error as err:
        logging.error("Database error: {}".format(err))
    except Exception as err:
        logging.error("Unexpected error: {}".format(err))
    finally:
        db.close()


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


if __name__ == '__main__':
    main()
