# -*- coding: utf-8 -*-
import os
import json
from typing import Dict, Tuple
from engine.jasper_report import OnesphereReportJasper
from utils.utils import today, ensure_directory_exist, ustr
import tempfile
from loguru import logger
from utils.constants import ENV_REPORTS_DIR


def compile_all_jrxml(reports_dir=ENV_REPORTS_DIR):
    REPORTS_DIR = os.getenv('ENV_REPORTS_DIR') or reports_dir
    r = OnesphereReportJasper()
    r.config(input_file=REPORTS_DIR)
    r.compile(write_jasper=True)


def compile_to_japser(jrxml_file: str, reports_dir=os.getenv('ENV_REPORTS_DIR')):
    REPORTS_DIR = reports_dir
    input_file = os.path.join(REPORTS_DIR, jrxml_file)
    r = OnesphereReportJasper()
    r.config(input_file=input_file)
    r.compile(write_jasper=True)


# FIXME: 报告中中文无法显示
def _raw_process_to_jasper_report(jrxml_file: str, data: Dict = None, file_format: str = 'pdf',
                                  reports_dir=ENV_REPORTS_DIR, output_fn: str = '') -> bytes:
    out_data = b''
    if not data:
        logger.error(f'{__name__}数据内容为空')
        return out_data
    REPORTS_DIR = reports_dir
    input_file = os.path.join(REPORTS_DIR, jrxml_file)
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(data).encode('utf-8'))
        f.seek(0)  # 回到初始位置
        r = OnesphereReportJasper()
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
        r.process_report(output_filename=output_fn)
        if output_fn:
            out_file.close()  # 关闭删除临时文件
            out_file = open(output_fn, 'rb')
        out_file.seek(0)
        out_data = out_file.read()
        out_file.close()
    return out_data


def process_to_jasper_report(jrxml_file: str, out_file: str = 'output.pdf', data=None,
                             reports_dir=os.getenv('ENV_REPORTS_DIR'),
                             raw=True) -> Tuple[bytes, str]:
    ret = b''
    out, file_format = out_file.split('.')
    if not out or not file_format:
        logger.error(f'{__name__}解析out_file格式错误，out_file: {out_file}')
        return ret, ''
    directory = os.path.join(reports_dir, f"{today().replace('-', '_')}/")
    try:
        ensure_directory_exist(directory)
    except Exception as e:
        logger.error(ustr(e))
        return ret, ''
    ff = os.path.join(directory, out_file)
    d = _raw_process_to_jasper_report(jrxml_file, reports_dir=reports_dir, data=data, file_format=file_format,
                                      output_fn=ff)
    if raw:
        return d, ''
    return d, ff
