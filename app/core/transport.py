"""
This file include all class definition of transport objects. 

These objects are meant to transport all sort of aggregated data to other module
of this app. 


API -> Core: 
    get me the results of question with id 1

Core -> BaseAnswer:
    compute the results for question 1 

    BaseAnswer -> HistogrammeQuerySet:
        compute the results for question 1 

    HistogrammeQuerySet -> Histogramme: 
        init yourself with question 1 and myself (QuerySet) as data

Core -> API:
    take this object (Histogramme)

API -> API: 
    serialize this object 

API -> front-end (HTTP): 
    take this serialized results (JSON)
"""
class CHART_TYPES:
    HISTOGRAMME = 'histogramme'
    PIE = 'pie'
    HORIZONTAL_BAR = 'horizontal_bar'
    VERTICAL_BAR = 'veritical_bar'


class ResultObject(object):
    def __init__(self, question, queryset):
        self.question = question
        self.queryset = queryset
        self.total_answers = float(queryset.count())
        self.max_id = 0
        self.sets = {}
        self.results = {}
        self.create_sets()

    def create_sets(self):
        self_klass = self.__class__.__name__
        raise NotImplementedError(
            '{klass} must implement `create_sets` method'.format(
                klass=self_klass)
        )

    def as_dict(self):
        return {
            'sets':     self.sets,
            'results':  self.results,
            'chart_type': self.chart_type
        }


class Histogramme(ResultObject):
    chart_type = CHART_TYPES.HISTOGRAMME
    def __init__(self, question, queryset, sets=5):
        self.mininum = question.min_number
        self.maximum = question.max_number
        self.set_number = sets
        super(Histogramme, self).__init__(question, queryset)

    def create_sets(self):
        gap = self.maximum - self.mininum
        gap /= self.set_number
        if int(self.total_answers) > 0:
            for i in range(0, self.set_number):
                int_min = gap * i
                int_max = gap * (i+1)

                qs = self.queryset.filter(value__gte=int_min, value__lt=int_max) 
                answers = float(qs.count())
                percentage =  answers / self.total_answers 
                percentage *= 100
                self.add_set(mininum=int_min, maximum=int_max, percentage=percentage)


    def add_set(self, mininum, maximum, percentage):
        set_id = self.get_next_id()
        set = {
            'min': mininum,
            'max': maximum
        }
        self.sets[set_id] = set
        self.results[set_id] = percentage

    def get_next_id(self):
        for set_id in self.sets.keys():
            self.max_id = max(self.max_id, int(set_id)) 
        return self.max_id + 1

class BarChart(ResultObject):
    def create_sets(self):
        for choice in self.question.choices():
            answers = self.queryset.filter(value=choice).count()
            self.add_set(choice, answers)

    def add_set(self, choice, value): 
        self.sets[choice.id] = {
            'name': choice.title
        }
        self.results[choice.id] = value

class HorizontalBarChart(BarChart):
    chart_type = CHART_TYPES.HORIZONTAL_BAR
    
class VerticalBarChart(BarChart):
    chart_type = CHART_TYPES.VERTICAL_BAR

class PieChart(BarChart):
    chart_type = CHART_TYPES.PIE



