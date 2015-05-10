from __future__ import print_function


class BoxPlotData(object):
    def __init__(self, category_title, measure_name):
        self._category_title = category_title
        self._measure_name = measure_name
        self._category_statistics = []

    @property
    def category_title(self):
        return self._category_title

    @property
    def measure_name(self):
        return self._measure_name

    def _measure_limit(self, stat_name, limit_func):
        return reduce(lambda x,y: limit_func(x,y),
            map(lambda s: s[stat_name], self._category_statistics))

    @property
    def min_measure(self):
        return self._measure_limit('min', min)

    @property
    def max_measure(self):
        return self._measure_limit('max', max)

    @property
    def measure_name_length(self):
        return len(self._measure_name)

    @property
    def category_title_length(self):
        return len(self._category_title)

    @property
    def max_category_name_length(self):
        return reduce(lambda x,y: max(x,y),
            map(lambda s: len(s['name']), self._category_statistics))

    def add_category_statistics(self, category_name, min,
        min_dispersion, location, max_dispersion, max, count):
        self._category_statistics.append({
            'name': category_name,
            'min': min,
            'min_dispersion': min_dispersion,
            'location': location,
            'max_dispersion': max_dispersion,
            'max': max,
            'count': count})


class BoxPlot(object):
    def __init__(self, data):
        self._data = data

    def _spaces(self, length):
        return ' ' * length

    def _spacing_for_measure_title(self):
        return max(0, self._measure_centre - self._measure_name_centre)

    def _spacing_for_measure_axis(self):
        return max(0, self._measure_name_centre - self._measure_centre)

    def _spacing_for_measure_axis_line(self):
        return (len(self._category_title) + self._spacing_for_measure_axis())

    @property
    def _negative_measure_length(self):
        if self._min_measure < 0:
            return abs(min(-1, self._max_measure) - self._min_measure + 1)
        return 0

    @property
    def _zero_measure_length(self):
        if self._min_measure < 0 and self._max_measure > 0:
            return 1
        return 0

    @property
    def _positive_measure_length(self):
        if self._max_measure > 0:
            return self._max_measure - max(1, self._min_measure) + 1
        return 0

    @property
    def _min_measure(self):
        return self._data.min_measure

    @property
    def _max_measure(self):
        return self._data.max_measure

    @property
    def _measure_length(self):
        return self._max_measure - self._min_measure + 1

    @property
    def _measure_centre(self):
        return self._measure_length/2

    @property
    def _measure_name_centre(self):
        return self._data.measure_name_length/2

    def _spacing_for_category_title(self):
        category_title_length = self._data.category_title_length
        max_title_length = self._data.max_category_name_length
        return (max(category_title_length, max_title_length) -
            category_title_length + 1)

    @property
    def _category_title(self):
        return (self._data.category_title +
            self._spaces(self._spacing_for_category_title()))

    @property
    def _title(self):
        return (self._category_title +
            self._spaces(self._spacing_for_measure_title()) +
            self._data.measure_name)

    @property
    def _sign_indicator(self):
        return ('-' * self._negative_measure_length +
            ' ' * self._zero_measure_length +
            '+' * self._positive_measure_length)

    @property
    def _sign_indicator_line(self):
        return (self._spaces(self._spacing_for_measure_axis_line()) +
            self._sign_indicator)

    @property
    def _number_lines(self):
        lines = []

        line = self._spaces(self._spacing_for_measure_axis_line())
        for i in range(self._min_measure, self._max_measure+1):
            line += str(abs(i))

        lines.append(line)

        return lines
