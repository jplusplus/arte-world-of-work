from django.db.models import query 
from app.core.transport import Histogramme, HorizontalBarChart, VerticalBarChart, PieChart

class ResultsQuerySet(query.QuerySet):
    def in_age(self, age_min=None, age_max=None):
        if age_max and age_min:
            return self.filter(user__userprofile__age__lte=age_max, user__userprofile__age__gte=age_min)
        return self

    def with_gender(self, gender=None):
        return self.filter(user__userprofile__gender=gender)

    def compute(self, question=None):
        if not question:
            raise AttributeError('compute method need a question to work properly')
        return self.get_transport_object(question)

    def get_transport_object(self, question=None):
        qs = self.filter(question=question)
        return self.__class__.transport_class(question, qs) 

class HistogrammeQuerySet(ResultsQuerySet):
    transport_class = Histogramme

class HorizontalBarChartQuerySet(ResultsQuerySet):
    transport_class = HorizontalBarChart

class VerticalBarChartQuerySet(ResultsQuerySet):
    transport_class = VerticalBarChart

class PieChartQuerySet(ResultsQuerySet):
    transport_class = PieChart
