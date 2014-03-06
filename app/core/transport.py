#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import Context, Template
from app.core.types import CHART_TYPES
import random 

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
            'sets':          self.sets,
            'results':       self.results,
            'chart_type':    self.chart_type,
            'total_answers': int(self.total_answers)
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

                answers = self.queryset.filter(value__gte=int_min, value__lt=int_max).count()
                percentage =  answers * 100.0 / self.total_answers
                percentage = int(percentage)
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
        if int(self.total_answers) > 0:
            for choice in self.question.choices():
                answers = self.queryset.filter(value=choice).count()
                percentage = answers * 100.0 / self.total_answers
                percentage = int(percentage)
                self.add_set(choice, percentage)

    def add_set(self, choice, value): 
        self.sets[choice.id] = {
            'title': choice.title
        }
        self.results[choice.id] = value

class HorizontalBarChart(BarChart):
    chart_type = CHART_TYPES.HORIZONTAL_BAR
    
class VerticalBarChart(BarChart):
    chart_type = CHART_TYPES.VERTICAL_BAR

class PieChart(BarChart):
    chart_type = CHART_TYPES.PIE

class DynamicFeedback(object):
    SENTENCES_PROFILE_MAPPING = {
        'living_country': _('persons living in {value}'),
        'native_country': _('persons from {value}'),
        'gender':         _('{value}'),
        'age':            _('aged {value} years')
    }

    def __init__(self, user, question):
        self.html_sentence = None
        self.profile       = user.userprofile
        self.question      = question

        # simple wrapper around the answer_type to use 
        class AnswerType(question.answer_type): 
            class Meta: 
                proxy=True
            pass
        # make him accessible for this instance    
        self.AnswerType = AnswerType
        self.create_html_sentence()

    def base_answer_model(self, AnswerType=None):
        if AnswerType.__name__ != 'BaseAnswer':
            return self.base_answer_model(AnswerType.__bases__[0])
        else:
            return AnswerType

    def create_html_sentence(self):
        AnswerType = self.AnswerType
        BaseAnswer = self.base_answer_model(AnswerType)
        myanswer   = None

        try:
            myanswer    = AnswerType.objects.get(question=self.question, 
                                                 user=self.profile.user).as_final()
        except BaseAnswer.DoesNotExist: 
            pass

        answers_pool = self.lookup_for_answers()

        all_answers     = answers_pool['all_answers']['set']
        profile_answers = answers_pool['profile_answers']
        if profile_answers:
            answers_set  = profile_answers['set']
            profile_attr = profile_answers['profile_attr']
        else:
            answers_set = all_answers

        total_number    = all_answers.count()

        if myanswer:
            similar_answers = answers_set.filter(value=myanswer.value)
            profile_attr    = None
            use_percentage  = self.is_percentage()
            if use_percentage:
                percentage =  float(similar_answers.count()) / total_number
                percentage = int(round(percentage*100))
                self.html_sentence = _(
                    '<strong>{value}%</strong> of '.format(
                        value=percentage))
            else:
                self.html_sentence = _('<strong>{value}</strong> '.format(
                    value=similar_answers.count()))

            if profile_attr:
                profile_value = getattr(self.profile, profile_attr, None)
                sentence = SENTENCES_PROFILE_MAPPING[profile_attr]
                if use_percentage and profile_attr == 'gender':
                    self.html_sentence += _('the ')
                self.html_sentence += sentence.format(value=profile_value)
            else:
                self.html_sentence += _('persons ')

        else:
            self.html_sentence = _(
                'Until this day <strong>{value}</strong> persons'.format(value=total_number)
            )

        self.html_sentence += _('answered like you')


    def lookup_for_answers(self):
        # will contain multiple answers set. It will help us to know what 
        answers_pool = {}

        all_answers = self.AnswerType.objects.filter(question=self.question)
        all_answers = all_answers.exclude(user=self.profile.user)

        answers_pool['all_answers'] = { 
            'set': all_answers
        }
        challenger = None
        challenger_attr = None

        for profile_attr in ('age', 'gender', 'living_country', 'native_country'):
            profile_value = getattr(self.profile, profile_attr, None)
            if profile_value != None:
                lookup_key = 'user__userprofile__{attr}'.format(
                    attr=profile_attr)
                filters = {
                    lookup_key: profile_value
                }
                set = all_answers.filter()

                is_new_challenger = (
                    (set.count() > 500) \
                    and \
                    (
                        (challenger == None) \
                        or  \
                        (
                            (challenger != None) \
                            and \
                            (set.count() > challenger.count())
                        )
                    )
                )

                if is_new_challenger:
                    challenger = set
                    challenger_attr = profile_attr

        answers_pool['profile_answers'] = {
            'set': challenger,
            'profile_attr': challenger_attr
        }
        return answers_pool

    def is_percentage(self):
        # will randomly decide if we should use percentage or count results 
        # Return boolean to tell if result type is percentage or not.
        choices = (True, False)
        return choices[ random.randint(0, len(choices) - 1) ]

# EOF