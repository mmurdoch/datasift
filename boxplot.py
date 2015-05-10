

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

    def _spacing_for_category_title(self):
        category_title_length = self._data.category_title_length
        max_title_length = self._data.max_category_name_length
        return (max(category_title_length, max_title_length) -
            category_title_length + 1)

    def _spacing_for_measure_title(self):
        max_measure = self._data.max_measure
        min_measure = self._data.min_measure
        return max(0, ((max_measure - min_measure + 1)/2 -
            self._data.measure_name_length/2))

    @property
    def title(self):
        return (self._data.category_title +
            self._spaces(self._spacing_for_category_title()) +
            self._spaces(self._spacing_for_measure_title()) +
            self._data.measure_name)
