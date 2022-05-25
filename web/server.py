# -*- coding: utf-8 -*-
import sqlite3

from loguru import logger
from typing import Optional
from asyncio import AbstractEventLoop
from web.routes import healthzCheckHandler, readinessCheckHandler, generate_report
from database import create_database_connect
from version import major_version, description, product_name
from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings
import os
from argument import ArgsService
from constants import ENV_REPORTS_DIR

ROOTDIR = os.path.dirname(os.path.realpath(__file__))
component_file = os.path.join(ROOTDIR, 'components.yaml')


def create_web_app() -> web.Application:
    # loop = asyncio.get_event_loop()
    ret: web.Application = web.Application(client_max_size=1024 * 1024 * 10)
    swagger = SwaggerDocs(
        ret,
        swagger_ui_settings=SwaggerUiSettings(path="/docs/", filter=True),
        title=f"{description}-接口文档",
        version=major_version,
        components=component_file
    )
    swagger.add_routes([web.get('/healthz', healthzCheckHandler),
                        web.get('/rediness', readinessCheckHandler),
                        web.post('/report/{report_type}', generate_report)
                        ])

    return ret


class HttpServer(object):
    def __init__(self, port=9110, *args, **kwargs):
        self._port = port
        self._app: web.Application = create_web_app()
        self._app['db']: Optional[sqlite3.Connection] = None
        self._app['args']: ArgsService = kwargs.get('raw_args')
        if kwargs.get('db_name', ''):
            # 创建数据库
            self._app['db'] = create_database_connect(kwargs.get('db_name'), kwargs.get('cache', False))

    def start(self, loop: Optional[AbstractEventLoop] = None):
        reports_dir = ENV_REPORTS_DIR or self._app['args'].reports_dir
        if os.path.isdir(reports_dir) and not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
        self.run(loop)

    def run(self, loop: Optional[AbstractEventLoop] = None):
        logger.info(f"[{product_name}] Http Server Start")
        web.run_app(self._app, host='0.0.0.0', port=self._port, access_log=logger, loop=loop)
        logger.info(f"[{product_name}] Http Server Stop")

    def close_database(self):
        if self._app['db']:
            db: sqlite3.Connection = self._app['db']
            db.close()

    def stop(self):
        self.close_database()
        return self._app.shutdown()
