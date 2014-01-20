"""
This module contains all django command and utility classes for our translation
sytem. This work pseudo system is inspired from django-modeltranslation library
and use the same paradigm to keep models safe from edition (reference bellow).


This is a pseudo "hybrid" system in the way we bind together classical django 
translation (recolted with gettext) and dynamic data.

**django-modeltranslation**

    https://django-modeltranslation.readthedocs.org/en/latest/

"""