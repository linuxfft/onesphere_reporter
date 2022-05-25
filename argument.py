# -*- coding: utf-8 -*-
import os
from tap import Tap


class ArgsCommon(Tap):
    reports_dir: str = os.path.join(os.getcwd(), 'reports')


class ArgsCli(ArgsCommon):  # Define console args
    pass


class ArgsService(ArgsCommon):  # Define console args
    port: int = 9090  # 服务端口
    cache: bool = False  # 是否基于缓存
    db_name: str = 'reporter.db'  # 数据库地址
