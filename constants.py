# -*- coding: utf-8 -*-

import os

import pytz

ENV_RUNTIME_ENV = os.getenv('ENV_RUNTIME_ENV', 'dev')

DEFAULT_TZ = pytz.timezone('Asia/Shanghai')

ENV_REPORTS_DIR = os.getenv('ENV_REPORTS_DIR', '')
ENV_HTTP_MAX_SIZE = int(os.getenv('ENV_HTTP_MAX_SIZE', '20'))  # http最大包大小，单位为mb
