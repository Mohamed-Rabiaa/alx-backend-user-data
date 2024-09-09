#!/usr/bin/env python3
"""
This module contains the auth class
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password

    Args:
        password (str): The password to hash

    Returns:
        (bytes): The hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
