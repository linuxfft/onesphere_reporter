# -*- coding: utf-8 -*-

import os
import pytz

ENV_RUNTIME_ENV = os.getenv('ENV_RUNTIME_ENV', 'dev')

DEFAULT_TZ = pytz.timezone('Asia/Shanghai')

ENV_REPORTS_DIR = os.getenv('ENV_REPORTS_DIR', '')
