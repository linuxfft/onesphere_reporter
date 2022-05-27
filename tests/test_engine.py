# -*- coding: utf-8 -*-
from unittest import TestCase
from engine.engine import process_to_jasper_report
import json
import os


class Test(TestCase):
    def test_process_to_jasper_report_pdf(self):
        reports_dir = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, 'reports'))
        with open(os.path.join(reports_dir, 'json_test.json')) as f:
            data = json.load(f)
        d = process_to_jasper_report(jrxml_file='json_test.jrxml', out_file='out.pdf', reports_dir=reports_dir,
                                     data=data, raw=False)
        self.fail()

    def test_process_to_jasper_report_html(self):
        reports_dir = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, 'reports'))
        with open(os.path.join(reports_dir, 'json_test.json')) as f:
            data = json.load(f)
        d = process_to_jasper_report(jrxml_file='json_test.jrxml', out_file='out.html', reports_dir=reports_dir,
                                     data=data, raw=False)
