# -*- coding: utf-8 -*-
from django.db.models.base import ModelBase
from django.utils.six import with_metaclass
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _


"""
Most parts come from django-modeltranslations. 

TranslationOptions are options to register some model fields as translatable

Translator is the base class to register associations of model and translations 
options (TranslationOptions)
"""
SUPPORTED_FIELDS = (
    fields.CharField, 
    fields.TextField,
)

class GettextFieldDescriptor(object):
    """
    Field wrapper (for __get__ method)
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = getattr(instance, self.field.name, None)
        if val is not None:
            return _(val)
        return None


class NONE:
    """
    Used for fallback options when they are not provided (``None`` can be
    given as a fallback or undefined value) or to mark that a nullable value
    is not yet known and needs to be computed (e.g. field default).
    """
    pass
class DescendantRegistered(Exception):
    pass

class FieldsAggregationMetaClass(type):
    """
    Metaclass to handle custom inheritance of fields between classes.
    """
    def __new__(cls, name, bases, attrs):
        attrs['fields'] = set(attrs.get('fields', ()))
        for base in bases:
            if isinstance(base, FieldsAggregationMetaClass):
                attrs['fields'].update(base.fields)
        attrs['fields'] = tuple(attrs['fields'])
        return super(FieldsAggregationMetaClass, cls).__new__(cls, name, bases, attrs)


class TranslationOptions(with_metaclass(FieldsAggregationMetaClass, object)): 
    def __init__(self, model):
        self.model = model
        self.fields = dict((f, set()) for f in self.fields)
        self.local_fields = dict((f, set()) for f in self.fields)

    def update(self, other):
        """
        Update with options from a superclass.
        """
        if other.model._meta.abstract:
            self.local_fields.update(other.local_fields)
        self.fields.update(other.fields)

    def add_translation_field(self, field, translation_field):
        """
        Add a new translation field to both fields dicts.
        """
        self.local_fields[field].add(translation_field)
        self.fields[field].add(translation_field)

    def get_field_names(self):
        """
        Return name of all fields that can be used in filtering.
        """
        return list(self.fields.keys())

    def __str__(self):
        local = tuple(self.local_fields.keys())
        inherited = tuple(set(self.fields.keys()) - set(local))
        return '%s: %s + %s' % (self.__class__.__name__, local, inherited)


class Translator(object):
    def __init__(self):
        self._registry = {}

    def parse_field(self, setting, field_name, default):
        """
        Extract result from single-value or dict-type setting like fallback_values.
        """
        if isinstance(setting, dict):
            return setting.get(field_name, default)
        else:
            return setting

    def register(self, model, opts_class=None, **options):
        opts = self._get_options_for_model(model, opts_class, **options)
        for field_name in opts.local_fields.keys():

            field = model._meta.get_field(field_name)
            ref_field_name = "ref_{field}".format(field=field_name)
            descriptor = GettextFieldDescriptor(field)
            setattr(model, field_name, descriptor)
            setattr(model, ref_field_name, field)


    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't registered, this will raise NotRegistered. If one of
        its subclasses is registered, DescendantRegistered will be raised.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            # Check if the model is actually registered (``get_options_for_model``
            # throws an exception if it's not).
            self.get_options_for_model(model)
            # Invalidate all submodels options and forget about
            # the model itself.
            for desc, desc_opts in list(self._registry.items()):
                if not issubclass(desc, model):
                    continue
                if model != desc and desc_opts.registered:
                    # Allowing to unregister a base would necessitate
                    # repatching all submodels.
                    raise DescendantRegistered(
                        'You need to unregister descendant "%s" before'
                        ' unregistering its base "%s"' %
                        (desc.__name__, model.__name__))
                del self._registry[desc]

    def get_registered_models(self, abstract=True):
        """
        Returns a list of all registered models, or just concrete
        registered models.
        """
        return [model for (model, opts) in self._registry.items()
                if opts.registered and (not model._meta.abstract or abstract)]

    def _get_options_for_model(self, model, opts_class=None, **options):
        """
        Returns an instance of translation options with translated fields
        defined for the ``model`` and inherited from superclasses.
        """
        if model not in self._registry:
            # Create a new type for backwards compatibility.
            opts = type("%sTranslationOptions" % model.__name__,
                        (opts_class or TranslationOptions,), options)(model)

            # Fields for translation may be inherited from abstract
            # superclasses, so we need to look at all parents.
            for base in model.__bases__:
                if not hasattr(base, '_meta'):
                    # Things without _meta aren't functional models, so they're
                    # uninteresting parents.
                    continue
                opts.update(self._get_options_for_model(base))

            # Cache options for all models -- we may want to compute options
            # of registered subclasses of unregistered models.
            self._registry[model] = opts

        return self._registry[model]

translator = Translator()