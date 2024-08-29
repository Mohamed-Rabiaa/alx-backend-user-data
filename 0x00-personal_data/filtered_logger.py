#!/usr/bin/env python3
"""
This module contains the filter_datum funtion
"""

import re
from typing import List


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
