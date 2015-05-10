from boxplot import BoxPlot
from boxplot import BoxPlotData
import unittest


class BoxPlotDataTest(unittest.TestCase):
    def test_max_category_name_length_no_stats(self):
        data = BoxPlotData('Name', 'Length')

        self.assertEquals(0, data.max_category_name_length)

    def test_max_measure_no_stats(self):
        data = BoxPlotData('Name', 'Length')

        self.assertEquals(0, data.max_measure)

    def test_min_measure_no_stats(self):
        data = BoxPlotData('Name', 'Length')

        self.assertEquals(0, data.min_measure)


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

        self.assertEquals(1, boxplot._spacing_for_measure_axis())
        self.assertEquals(8, boxplot._spacing_for_measure_axis_line())
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

        self.assertEquals(3, boxplot._spacing_for_measure_axis())
        self.assertEquals(11, boxplot._spacing_for_measure_axis_line())
        self.assertEquals(5, boxplot._negative_measure_length)
        self.assertEquals(0, boxplot._zero_measure_length)
        self.assertEquals(0, boxplot._positive_measure_length)
        #                  Emotion Positivity
        self.assertEquals('           -----', boxplot._sign_indicator_line)
        #                             1
        #                             09876
        #                  Anger      | -:|

    def test_sign_indicator_line_spanning_zero(self):
        data = BoxPlotData('Emotion', 'Positivity')
        data.add_category_statistics('Worry', -5, -3, -1, 2, 4, 19)

        boxplot = BoxPlot(data)

        self.assertEquals(0, boxplot._spacing_for_measure_axis())
        self.assertEquals(8, boxplot._spacing_for_measure_axis_line())
        self.assertEquals(5, boxplot._negative_measure_length)
        self.assertEquals(1, boxplot._zero_measure_length)
        self.assertEquals(4, boxplot._positive_measure_length)
        #                  Emotion Positivity
        self.assertEquals('        ----- ++++', boxplot._sign_indicator_line)
        #                          5432101234
        #                  Worry   | --:--- |

    def test_single_digit_number_line(self):
        data = BoxPlotData('Emotion', 'Positivity')
        data.add_category_statistics('Worry', -5, -3, -1, 2, 4, 19)

        boxplot = BoxPlot(data)

        #                  Emotion Positivity
        #                          ----- ++++
        self.assertEquals('        5432101234', boxplot._number_lines[0])
        #                  Worry   | --:--- |

    def test_double_digit_number_line(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -20, -2, 0, 2, 17, 18)

        boxplot = BoxPlot(data)

        #                  Name                  Quality
        #                       -------------------- +++++++++++++++++
        self.assertEquals('     21111111111                   11111111',
            boxplot._number_lines[0])
        self.assertEquals('     09876543210987654321012345678901234567',
            boxplot._number_lines[1])
        #                  a    |                 --:--              | (18)

    def test_double_digit_number_line_count(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -53, -2, 0, 30, 39, 18)

        boxplot = BoxPlot(data)

        self.assertEquals(2, boxplot._number_line_count)

    def test_triple_digit_number_line_count(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -5, -2, 0, 830, 909, 18)

        boxplot = BoxPlot(data)

        self.assertEquals(3, boxplot._number_line_count)

    def test_single_digit_number_line_multipler(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -5, -2, 0, 8, 9, 18)

        boxplot = BoxPlot(data)

        self.assertEquals([1], boxplot._number_line_multipliers)

    def test_double_digit_number_line_multipler(self):
        data = BoxPlotData('Name', 'Quality')
        data.add_category_statistics('a', -25, -2, 0, 8, 9, 18)

        boxplot = BoxPlot(data)

        self.assertEquals([10, 1], boxplot._number_line_multipliers)

    def test_digit(self):
        self.assertEquals('0', BoxPlot._digit(1,    0))
        self.assertEquals('1', BoxPlot._digit(1,    1))
        self.assertEquals('1', BoxPlot._digit(1,   -1))
        self.assertEquals('9', BoxPlot._digit(1,    9))

        self.assertEquals('0', BoxPlot._digit(1,   10))
        self.assertEquals('9', BoxPlot._digit(1,   19))
        self.assertEquals('8', BoxPlot._digit(1,  -98))

        self.assertEquals('1', BoxPlot._digit(10,  19))
        self.assertEquals('6', BoxPlot._digit(10, -64))

        self.assertEquals(' ', BoxPlot._digit(10,   1))

    def test_category_line(self):
        data = BoxPlotData('Nm', 'Quality')
        data.add_category_statistics('Animal', -10, -2, 0, 2, 10, 18)

        boxplot = BoxPlot(data)

        #                  Nm            Quality', boxplot._title)
        #                         ---------- ++++++++++
        #                         1                   1
        #                         098765432101234567890
        self.assertEquals('Animal |       --:--       | (18)',
            boxplot._category_lines[0])


if __name__ == '__main__':
    unittest.main()
