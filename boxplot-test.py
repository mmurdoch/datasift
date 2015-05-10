from boxplot import BoxPlot
from boxplot import BoxPlotData
import unittest


class BoxPlotTest(unittest.TestCase):
    def test_title_longer_than_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -2, -1, 0, 1, 2, 6)

        boxplot = BoxPlot(data)

        self.assertEquals('Name Quality', boxplot.title)
        #                        -- ++
        #                        21012
        #                  a     |-:-| (6)

    def test_title_shorter_than_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -10, -2, 0, 2, 10, 18)

        boxplot = BoxPlot(data)

        self.assertEquals('Name         Quality', boxplot.title)
        #                        ---------- ++++++++++
        #                        1                   1
        #                        098765432101234567890
        #                  a     |       --:--       | (18)

    def test_title_for_positive_only_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', 2, 4, 8, 10, 16, 8)

        boxplot = BoxPlot(data)

        self.assertEquals('Name      Quality', boxplot.title)
        #                        +++++++++++++++
        #                                1111111
        #                        234567890123456
        #                  a     | ----:--     | (18)

    def test_title_for_long_category_names(self):
        data = BoxPlotData('Nm', 'Quality')
        data.add_category_statistics('Animal', -10, -2, 0, 2, 10, 18)

        boxplot = BoxPlot(data)

        self.assertEquals('Nm            Quality', boxplot.title)
        #                         ---------- ++++++++++
        #                         1                   1
        #                         098765432101234567890
        #                  Animal |       --:--       | (18)

if __name__ == '__main__':
    unittest.main()
