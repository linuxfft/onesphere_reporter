# -*- coding: utf-8 -*-
import os
import json
from typing import Dict
from pyreportjasper import PyReportJasper
from pyreportjasper.config import Config
from pyreportjasper.report import Report
import tempfile
from loguru import logger
from constants import ENV_REPORTS_DIR


def compile_all_jrxml(reports_dir=ENV_REPORTS_DIR):
    REPORTS_DIR = os.getenv('ENV_REPORTS_DIR') or reports_dir
    r = PyReportJasper()
    r.config(input_file=REPORTS_DIR)
    r.compile(write_jasper=True)


def compile_to_japser(jrxml_file: str, reports_dir=os.getenv('ENV_REPORTS_DIR')):
    REPORTS_DIR = reports_dir
    input_file = os.path.join(REPORTS_DIR, jrxml_file)
    r = PyReportJasper()
    r.config(input_file=input_file)
    r.compile(write_jasper=True)


# FIXME: 报告中中文无法显示
def _raw_process_to_jasper_report(jrxml_file: str, data: Dict = None, file_format: str = 'pdf',
                                  reports_dir=ENV_REPORTS_DIR) -> bytes:
    out_data = b''
    if not data:
        logger.error(f'{__name__}数据内容为空')
        return out_data
    REPORTS_DIR = reports_dir
    input_file = os.path.join(REPORTS_DIR, jrxml_file)
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(data).encode('utf-8'))
        f.seek(0)  # 回到初始位置
        r = PyReportJasper()
        conn = {
            'driver': 'json',
            'data_file': f.name,
        }
        out_file = tempfile.NamedTemporaryFile(suffix=f'.{file_format}')
        o, file_format = out_file.name.split('.')
        r.config(input_file=input_file,
                 output_file=o,
                 locale='zh_CN',
                 output_formats=[file_format],
                 db_connection=conn
                 )
        r.process_report()
        out_file.seek(0)
        out_data = out_file.read()
        out_file.close()  # 关闭删除临时文件
    return out_data


def process_to_jasper_report(jrxml_file: str, out_file: str = 'output.pdf', data=None,
                             reports_dir=os.getenv('ENV_REPORTS_DIR'),
                             raw=True) -> str:
    ret = ''
    out, file_format = out_file.split('.')
    if not out or not file_format:
        logger.error(f'{__name__}解析out_file格式错误，out_file: {out_file}')
        return ret
    d = _raw_process_to_jasper_report(jrxml_file, reports_dir=reports_dir, data=data, file_format=file_format)
    str_d = bytes.decode(d, encoding='utf-8')
    if raw:
        return str_d
    ff = os.path.join(reports_dir, out_file)
    with open(ff, 'w+b') as f:
        f.write(d)
    return str_d
