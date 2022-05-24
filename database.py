# -*- coding: utf-8 -*-
import sqlite3
import os


def create_database_connect(name: str, cache: bool) -> sqlite3.Connection:
    if cache:
        name = ':memory:'
    else:
        dir = os.path.dirname(os.path.abspath(name))
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    con = sqlite3.connect(name)
    return con
