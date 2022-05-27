# -*- coding: utf-8 -*-
import os.path

from pyreportjasper import PyReportJasper
from pyreportjasper.report import Report
import jpype
from utils.utils import today, ensure_directory_exist, ustr


class OnesphereReport(Report):

    def export_html(self, output_file: str = 'out.html'):
        self.JasperExportManager.exportReportToHtmlFile(self.jasper_print,
                                                        jpype.JString(output_file))

    def export_pdf_file(self, output_file: str = 'out.pdf'):
        self.JasperExportManager.exportReportToPdfFile(self.jasper_print,
                                                       jpype.JString(output_file))


class OnesphereReportJasper(PyReportJasper):
    def __init__(self, *args, **kwargs):
        super(OnesphereReportJasper, self).__init__(*args, **kwargs)
        self.FORMATS = PyReportJasper.FORMATS + ('html',)

    def process_report(self, output_filename: str = ''):
        ret = need_html_format = need_pdf_format = False
        formats = self.config.outputFormats
        if 'html' in formats:
            self.config.outputFormats.remove('html')
            need_html_format = True
        if 'pdf' in formats:
            self.config.outputFormats.remove('pdf')
            need_pdf_format = True
        if len(formats):
            ret = super(OnesphereReportJasper, self).process_report()
        if output_filename:
            ensure_directory_exist(os.path.dirname(output_filename))
        if need_html_format:
            report = OnesphereReport(self.config, self.config.input)
            report.fill()
            report.export_html(output_file=output_filename or f'{self.config.output}.html')
        if need_pdf_format:
            report = OnesphereReport(self.config, self.config.input)
            report.fill()
            report.export_pdf_file(output_file=output_filename or f'{self.config.output}.pdf')
        return ret
