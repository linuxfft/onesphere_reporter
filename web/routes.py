# -*- coding: utf-8 -*-
from http import HTTPStatus
from typing import Dict
from aiohttp import web


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
            description: Expected response to a valid request
        """
    return web.Response(status=HTTPStatus.NO_CONTENT)
