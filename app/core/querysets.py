from django.db.models import query 
from app.core.transport import Histogramme, BarChart

class ResultsQuerySet(query.QuerySet):
    def in_age(self, age_min=None, age_max=None):
        if age_max and age_min:
            return self.filter(user__profile__age__lte=age_max, user__profile__age__gte=age_min)
        return self

    def with_gender(self, gender=None):
        return self.filter(user__profile__gender=gender)

    def compute(self, question=None):
        if not question:
            raise AttributeError('compute method need a question to work properly')
        return self.get_transport_object(question)

    def get_transport_object(self, question=None):
        qs = self.filter(question=question)
        return self.transport_class(question, qs)

class HistogrammeQuerySet(ResultsQuerySet):
    transport_class = Histogramme


class BarChartQuerySet(ResultsQuerySet):
    transport_class = BarChart