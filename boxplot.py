

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

    def _spaces_for_measure_title(self):
        max_measure = self._data.max_measure
        min_measure = self._data.min_measure
        return ' ' * (abs(max_measure - min_measure)/2 - len(self._data.category_title)/2)

    def _spaces_for_category_title(self):
        max_title_length = self._data.max_category_name_length
        category_title = self._data.category_title
        return ' ' * (max_title_length - len(category_title) + 1)

    @property
    def title(self):
        return (self._data.category_title +
            self._spaces_for_category_title() + ' ' +
            self._spaces_for_measure_title() + self._data.measure_name)
