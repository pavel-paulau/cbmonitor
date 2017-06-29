import os
from random import randint
from tempfile import TemporaryDirectory
from unittest import TestCase

import pandas
from PIL import Image

from cbmonitor.reports.plot import plot_as_png


class ChartTest(TestCase):

    def verify_image(self, filename: str):
        img = Image.open(filename)
        img.verify()

        self.assertEqual(img.width, 1000)
        self.assertEqual(img.height, 500)
        self.assertEqual(img.format, 'PNG')

    @staticmethod
    def new_series() -> pandas.Series:
        return pandas.Series([randint(-i, i) for i in range(1000)])

    def test_series(self):
        tmp_dir = TemporaryDirectory()
        filename = os.path.join(tmp_dir.name, 'img.png')

        series = self.new_series()

        plot_as_png(filename=filename,
                    series=[series, series],
                    labels=['label', 'label'],
                    colors=['#51A351', '#f89406'],
                    ylabel='label',
                    chart_type='',
                    rebalances=[[250, 750]])

        self.verify_image(filename)

    def test_percentiles(self):
        tmp_dir = TemporaryDirectory()
        filename = os.path.join(tmp_dir.name, 'img.png')

        series = self.new_series()

        for chart_type in '_lt90', '_gt80', '_histo':
            plot_as_png(filename=filename,
                        series=[series, series],
                        labels=['label', 'label'],
                        colors=['#51A351', '#f89406'],
                        ylabel='label',
                        chart_type=chart_type,
                        rebalances=[])

            self.verify_image(filename)
