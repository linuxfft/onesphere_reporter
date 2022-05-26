# -*- coding: utf-8 -*-
import os
import base64
from http import HTTPStatus
from typing import Dict
from aiohttp import web
from loguru import logger
from pprint import pformat
from utils.constants import ENV_REPORTS_DIR
from engine.engine import process_to_jasper_report
from utils.utils import ustr


# FIXME: swagger库 bug, 第一个参数名必须为request
async def healthzCheckHandler(request: web.Request) -> web.Response:
    """
        Optional route description
        ---
        summary: 健康检查
        tags:
          - availability
        responses:
          '204':
            description: Expected response to a valid request
        """
    return web.Response(status=HTTPStatus.NO_CONTENT)


# FIXME: swagger库 bug, 第一个参数名必须为request
async def readinessCheckHandler(request: web.Request) -> web.Response:
    """
        Optional route description
        ---
        summary: 可读性检查
        tags:
          - availability
        responses:
          '204':
            description: Expected response to a valid request
        """
    return web.Response(status=HTTPStatus.NO_CONTENT)


# FIXME: swagger库 bug, 第一个参数名必须为request
async def generate_report(request: web.Request, report_type: str = 'calibrate', body: Dict = {}) -> web.Response:
    """
        Optional route description
        ---
        summary: 生成报告
        parameters:
        - name: report_type
          in: path
          description: 报告类型
          required: true
          schema:
            type: string
            enum:
            - calibrate
          example: calibrate
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/generateReportReq"
        tags:
            - report
        responses:
          '201':
            description: 返回信息
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/generateReportResp"
        """
    raw = True
    data = {'file_path': '', 'file_data': ''}
    if report_type != 'calibrate':
        logger.error(f'报告类型不支持,当前只支持 calibrate, report type: {report_type}')
        return web.Response(status=HTTPStatus.BAD_REQUEST)
    body = await request.json()
    report_dir = ENV_REPORTS_DIR or request.app['args'].reports_dir
    render_data = body.get('data', {})
    jrxml_file = os.path.join(report_dir, body.get('jrxml_file'))
    if not os.path.exists(jrxml_file):
        msg = f'{jrxml_file} 不存在'
        logger.error(f'{generate_report.__name__} error: {msg}')
        return web.json_response(status=HTTPStatus.BAD_REQUEST, data={'error': msg, 'data': data})
    output_file = body.get('output_file')
    if output_file:
        raw = False
    logger.debug(f'{generate_report.__name__} 收到需要渲染数据: {pformat(render_data, indent=4)}')
    logger.debug(f'{generate_report.__name__} 收到需要jrxml: {jrxml_file}')
    try:
        d, directory = process_to_jasper_report(jrxml_file, output_file, data=render_data, reports_dir=report_dir,
                                                raw=raw)
        if not directory:
            msg = f'process_to_jasper_report 失败'
            return web.json_response(status=HTTPStatus.BAD_GATEWAY, data={'error': msg, 'data': data})
        base64_data = base64.b64encode(d)
    except Exception as e:
        msg = ustr(e)
        return web.json_response(status=HTTPStatus.BAD_GATEWAY, data={'error': msg, 'data': data})
    fn = os.path.join(directory, output_file)
    logger.debug(f'{generate_report.__name__} 渲染输出路径: {fn}')
    data['file_data'] = str(base64_data)
    data['file_path'] = fn
    return web.json_response(status=HTTPStatus.CREATED, data={'data': data})
