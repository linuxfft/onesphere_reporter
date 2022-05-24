# -*- coding: utf-8 -*-
import os
import sys
from typing import Optional
import signal
from web.server import HttpServer
from argument import ArgsService
from loguru import logger
from constants import ENV_RUNTIME_ENV
from utils import check_is_dev

if ENV_RUNTIME_ENV == ['prod', 'PROD', 'production']:
    logger.add('onesphere/reporter.log', rotation='1 days', level='INFO',
               encoding='utf-8', enqueue=True)  # 文件日誌
if check_is_dev():
    logger.add(sys.stdout, format="<r>{time}</r>: <lvl>{level}</lvl> <g>{message}</g>", level='INFO')

args = ArgsService().parse_args()
server: Optional[HttpServer] = None


def handler(signum, frame, *args, **kwargs):
    logger.info(f'收到信号: {signum}')
    server.stop()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    server = HttpServer(port=args.port, db_name=os.getenv('ENV_DATABASE_NAME', None) or args.db_name, cache=args.cache,
                        raw_args=args)
    server.run()
