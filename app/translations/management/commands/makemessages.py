#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:05
# Last Modified time: 2014-04-10 12:54:44
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
#
# Most parts of this translation module come from [django-modeltranslations](1) 
# project distibuted under the following copyright:
# 
# Copyright (c) 2012, 2011, 2010, 2009, Peter Eschler, Dirk Eschler
# All rights reserved.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# 1: https://github.com/deschler/django-modeltranslation

'''
Overrides the django `makemessages` command to collect also i18n strings with 
a grunt task also called "makemessages" 

For more information about the grunt task check the Gruntfile.coffee at the 
project root
'''
from django.core.management.commands.makemessages \
    import Command as BaseMakeMessages
from optparse \
    import make_option
import os

def grunt(cmd): 
    os.system('grunt %s'  % cmd)

class Command(BaseMakeMessages):
    option_list = BaseMakeMessages.option_list + (
        make_option('--static-only', default=False, dest='static_only', 
            help='Extract only the static locales (for angular application)',
            action='store_true'),
    )

    help = ("Will extract the i18n strings from the project and write them into"
            "conf/locale for .po files (extracted by django makemessages base " 
            "command) and in webapp/static/locales/ for static app translation")

    def handle_noargs(self, *args, **options):
        static_only = options.get('static_only')
        grunt('makemessages')
        if not static_only:
            super(Command, self).handle_noargs(*args, **options)

