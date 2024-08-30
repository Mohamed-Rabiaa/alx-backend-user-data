#!/usr/bin/env python3
"""
This module contains the hash_password function
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes a password and return it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
