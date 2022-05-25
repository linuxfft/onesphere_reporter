# -*- coding: utf-8 -*-
from constants import ENV_RUNTIME_ENV


def check_is_dev() -> bool:
    return ENV_RUNTIME_ENV in ['dev', 'DEV', 'development']
