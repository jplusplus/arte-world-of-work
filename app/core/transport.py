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
from django.utils.translation import ungettext, ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import fields
from django.template import loader, Context, Template
from django.template.loader import render_to_string
from django_countries import countries
from app.core.types import CHART_TYPES
import random

class ResultObject(object):
    def __init__(self, question, queryset):
        self.question = question
        self.queryset = queryset
        self.total_answers = queryset.count()
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
            'total_answers': self.total_answers
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
                percentage =  answers * 100.0 / float(self.total_answers)
                percentage = int(percentage + 0.5)
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
    def __init__(self, question, queryset):
        super(BarChart, self).__init__(question, queryset)
        self.check_if_multiple()

    def create_sets(self):
        if int(self.total_answers) > 0:
            for choice in self.question.choices():
                answers = self.queryset.filter(value=choice)
                percentage = answers.count() / float(self.total_answers)
                percentage = int(percentage*100+0.5)
                self.add_set(choice, percentage)

    def add_set(self, choice, value): 
        self.sets[choice.id] = { 
            'title': choice.title
        }
        self.results[choice.id] = value

    def check_if_multiple(self):
        if self.contains_multiple_answer():
            # we recompute total answers, we need to be sure to count every 
            self.total_answers = 0
            for choice in self.question.choices():
                self.total_answers += self.queryset.filter(value=choice).count()

    def contains_multiple_answer(self):
        answer_type = self.question.__class__.answer_type
        value_field = answer_type._meta.get_field('value')
        return hasattr(value_field, 'm2m_db_table')

class HorizontalBarChart(BarChart):
    chart_type = CHART_TYPES.HORIZONTAL_BAR
    
class VerticalBarChart(BarChart):
    chart_type = CHART_TYPES.VERTICAL_BAR

class PieChart(BarChart):
    chart_type = CHART_TYPES.PIE

class DynamicFeedback(object):
    def __init__(self, user=None, 
                       question=None, 
                       use_percentage=None):

        self.AnswerType      = None
        self.html_sentence   = None
        self.profile         = user.userprofile
        self.question        = question
        self._use_percentage = use_percentage
        self.AnswerType      = self.question.answer_type
        self.create_html_sentence()


    def get_base_answer_model(self):
        return self.base_answer_model(self.AnswerType)

    def base_answer_model(self, AnswerType=None):
        if AnswerType.__name__ != 'BaseAnswer':
            return self.base_answer_model(AnswerType.__bases__[0])
        else:
            return AnswerType

    def create_html_sentence(self):
        myanswer   = None
        BaseAnswer = self.get_base_answer_model()
        try:
            myanswer = BaseAnswer.objects.get(question=self.question, 
                user=self.profile.user)
            myanswer = myanswer.as_final()
        except BaseAnswer.DoesNotExist: 
            pass

        answers_pool    = self.lookup_for_answers()
        all_answers     = answers_pool['all_answers']
        profile_answers = answers_pool['profile_answers']
        answers_set     = profile_answers['set']
        profile_attr    = profile_answers['profile_attr']
        
        if answers_set == None:
            answers_set = all_answers

        self.total_answers = all_answers.count()

        context_dict = {
            'total_number':        answers_set.count(),
            'profile_attr':        profile_attr,
            'profile_attr_value':  self.get_profile_value(profile_attr),
            'use_profile_attr':    profile_attr != None,
        }

        if myanswer and context_dict['total_number'] > 0:
            similar_answers = self.get_similar(answers_set, myanswer)
            answer_count    = similar_answers.count()
            if self.is_percentage(context_dict):
                percentage = answer_count / float(context_dict['total_number'])
                context_dict['value'] = int(percentage*100+0.5)
                rendered = render_to_string('dynamic_feedback_percentage.dj.html', context_dict)
            else:
                context_dict['value'] = answer_count
                rendered = render_to_string('dynamic_feedback_count.dj.html', context_dict)
        else: 
            rendered = render_to_string('dynamic_feedback_generic.dj.html', context_dict)
        self.html_sentence = rendered
        return self.html_sentence

    def get_profile_value(self, profile_attr):
        if profile_attr == None:
            return None 
        value = getattr(self.profile, profile_attr, None)
        if profile_attr in ('living_country', 'native_country'):
            value = countries.name(value)
        return value

    def get_similar(self, answers_set, myanswer):
        value = myanswer.value
        if hasattr(value, 'all'):
            similar_answers = answers_set.filter(value__pk=value.values('pk'))
        else:
            similar_answers = answers_set.filter(value=value)
        return similar_answers

    def lookup_for_answers(self):
        BaseAnswer = self.get_base_answer_model()
        # will contain multiple answers set. It will help us to know what 
        answers_pool = {}
        # challenger represents the answer set to use for this dynamic feedback
        # it can be understood as: the best answer set that fit to with the 
        # given user profile `self.profile`
        challenger = None
        challenger_attr = None

        all_answers = self.AnswerType.objects.filter(question=self.question)
        all_answers = all_answers.exclude(user=self.profile.user)

        answers_pool['all_answers'] = all_answers

        for profile_attr in ('age', 'gender', 'living_country', 'native_country'):
            profile_value = getattr(self.profile, profile_attr, None)
            if profile_value != None:
                lookup_key = 'user__userprofile__{attr}'.format(
                    attr=profile_attr)
                filters = {
                    lookup_key: profile_value
                }
                set = all_answers.filter(**filters)
                is_new_challenger = (
                    (set.count() >= 50) \
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

    def is_percentage(self, context):
        # will randomly decide if we should use percentage or count results 
        # Return boolean to tell if result type is percentage or not.
        if self._use_percentage != None:
            use_percentage = self._use_percentage
        else:
            if self.question.typology == 'typed_number':
                use_percentage = False
            elif not context['use_profile_attr']:
                use_percentage = False
            else: 
                choices = (True, False)
                use_percentage = choices[ random.randint(0, len(choices) - 1) ]
        return use_percentage

    def as_dict(self):
        return {
            'question_id'  : self.question.pk,
            'total_answers': self.total_answers,
            'html_sentence': self.html_sentence,
            'type': 'feedback',
            'sub_type': 'dynamic' 
        }

# EOF