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

class Histogramme(object):
    def __init__(self, question, queryset, sets=5):
        super(Histogramme, self).__init__()
        self.mininum = question.min_number
        self.maximum = question.max_number
        self.max_id = 0
        self.queryset = queryset
        self.total_answers = float(queryset.count())
        self.set_number = sets
        self.sets = {}
        self.results = {}
        self.create_sets()

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


class BarChart(object):
    def __init__(self, question, queryset):
        pass
    

