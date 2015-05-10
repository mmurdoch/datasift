from boxplot import BoxPlot
from boxplot import BoxPlotData
import unittest


class BoxPlotTest(unittest.TestCase):
    def test_measure_name_even_length(self):
        data = BoxPlotData('Name', 'Length')
        data.add_category_statistics('a', -2, -1, 0, 1, 2, 6)

        boxplot = BoxPlot(data)

        self.assertEquals(1, boxplot._spacing_for_category_title())
        self.assertEquals(0, boxplot._spacing_for_measure_title())
        self.assertEquals('Name Length', boxplot._title)
        #                       -- ++
        #                       21012
        #                  a    |-:-| (6)

    def test_title_longer_than_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -2, -1, 0, 1, 2, 6)

        boxplot = BoxPlot(data)

        self.assertEquals(1, boxplot._spacing_for_category_title())
        self.assertEquals(0, boxplot._spacing_for_measure_title())
        self.assertEquals('Name Quality', boxplot._title)
        #                        -- ++
        #                        21012
        #                  a     |-:-| (6)

    def test_title_shorter_than_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -10, -2, 0, 2, 10, 18)

        boxplot = BoxPlot(data)

        self.assertEquals(1, boxplot._spacing_for_category_title())
        self.assertEquals(7, boxplot._spacing_for_measure_title())
        self.assertEquals('Name        Quality', boxplot._title)
        #                       ---------- ++++++++++
        #                       1                   1
        #                       098765432101234567890
        #                  a    |       --:--       | (18)

    def test_title_for_positive_only_statistics(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', 2, 4, 8, 10, 16, 8)

        boxplot = BoxPlot(data)

        self.assertEquals(1, boxplot._spacing_for_category_title())
        self.assertEquals(4, boxplot._spacing_for_measure_title())
        self.assertEquals('Name     Quality', boxplot._title)
        #                       +++++++++++++++
        #                               1111111
        #                       234567890123456
        #                  a    | ----:--     | (18)

    def test_title_for_long_category_names(self):
        data = BoxPlotData('Nm', 'Quality')
        data.add_category_statistics('Animal', -10, -2, 0, 2, 10, 18)

        boxplot = BoxPlot(data)

        self.assertEquals(5, boxplot._spacing_for_category_title())
        self.assertEquals(7, boxplot._spacing_for_measure_title())
        self.assertEquals('Nm            Quality', boxplot._title)
        #                         ---------- ++++++++++
        #                         1                   1
        #                         098765432101234567890
        #                  Animal |       --:--       | (18)

    def test_positive_sign_indicator_line(self):
        data = BoxPlotData('Animal', 'Height (cm)')
        data.add_category_statistics('Cat', 5, 5, 7, 9, 12, 250)

        boxplot = BoxPlot(data)

        self.assertEquals(1, boxplot._spacing_for_sign_indicator())
        self.assertEquals(8, boxplot._spacing_for_sign_indicator_line())
        self.assertEquals(0, boxplot._negative_measure_length)
        self.assertEquals(0, boxplot._zero_measure_length)
        self.assertEquals(8, boxplot._positive_measure_length)
        #                  Animal Height (cm)
        self.assertEquals('        ++++++++', boxplot._sign_indicator_line)
        #                               111
        #                          56789012
        #                  Cat     |-:--  |

    def test_negative_sign_indicator_line(self):
        data = BoxPlotData('Emotion', 'Positivity')
        data.add_category_statistics('Anger', -10, -8, -7, -6, -6, 43)

        boxplot = BoxPlot(data)

        self.assertEquals(3, boxplot._spacing_for_sign_indicator())
        self.assertEquals(11, boxplot._spacing_for_sign_indicator_line())
        self.assertEquals(5, boxplot._negative_measure_length)
        self.assertEquals(0, boxplot._zero_measure_length)
        self.assertEquals(0, boxplot._positive_measure_length)
        #                  Emotion Positivity
        self.assertEquals('           -----', boxplot._sign_indicator_line)
        #                             1
        #                             09876
        #                  Anger      | -:|

# neg
# Category title length: 8
# Spacing for sign indicator: 3


if __name__ == '__main__':
    unittest.main()
