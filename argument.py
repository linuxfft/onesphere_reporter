# -*- coding: utf-8 -*-

from tap import Tap


class ArgsCommon(Tap):
    reports_dir: str = '/opt/reports'


class ArgsCli(ArgsCommon):  # Define console args
    pass


class ArgsService(ArgsCommon):  # Define console args
    port: int = 9090  # 服务端口
    cache: bool = False  # 是否基于缓存
    db_name: str = 'reporter.db'  # 数据库地址
