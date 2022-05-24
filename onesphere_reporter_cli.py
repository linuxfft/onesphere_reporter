# -*- coding: utf-8 -*
import os
import sys
from loguru import logger

from constants import ENV_RUNTIME_ENV
from utils import check_is_dev
from argument import ArgsCli


if ENV_RUNTIME_ENV == ['prod', 'PROD', 'production']:
    logger.add('onesphere/reporter.log', rotation='1 days', level='INFO',
               encoding='utf-8', enqueue=True)  # 文件日誌
if check_is_dev():
    logger.add(sys.stdout, format="<r>{time}</r>: <lvl>{level}</lvl> <g>{message}</g>", level='INFO')

args = ArgsCli().parse_args()

if __name__ == '__main__':
    print()
