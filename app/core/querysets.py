#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 12:25:06
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

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
