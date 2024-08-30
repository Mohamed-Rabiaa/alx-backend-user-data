#!/usr/bin/env python3
"""
This module contains the hash_password and is_valid functions
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes a password and return it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
