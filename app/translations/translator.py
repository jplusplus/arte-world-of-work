# -*- coding: utf-8 -*-
from django.db.models.base import ModelBase
from django.utils.six import with_metaclass
from django.db.models import fields
from django.db.models.signals import post_init
from django.utils.translation import gettext as _
from .errors import *

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

def create_field(model, field_name):
    field = model._meta.get_field(field_name)
    field_cls  = field.__class__

    if not isinstance(field, SUPPORTED_FIELDS):
        raise ImproperlyConfigured(
            '%s is not supported by modeltranslation.' % field_cls.__name__)

    ref_field = field_cls()
    return ref_field


def bind_translation_fields(model, opts): 
    """
    Monkey patch the original model class to change every translatable field name 
    in database. 

    model.<field_name> will become model._<field_name> 
    """

    for field_name in opts.local_fields.keys():
        ref_field = create_field(model=model, field_name=field_name)
        ref_field_name = '_%s' % field_name

        model.add_to_class(ref_field_name, ref_field)
        opts.add_translation_field(field_name, ref_field)

def delete_mt_init(sender, instance, **kwargs):
    if hasattr(instance, '_mt_init'):
        del instance._mt_init


def patch_clean_fields(model):
    """
    Patch clean_fields method to handle different form types submission.
    """
    old_clean_fields = model.clean_fields

    def new_clean_fields(self, exclude=None):
        if hasattr(self, '_mt_form_pending_clear'):
            # Some form translation fields has been marked as clearing value.
            # Check if corresponding translated field was also saved (not excluded):
            # - if yes, it seems like form for MT-unaware app. Ignore clearing (left value from
            #   translated field unchanged), as if field was omitted from form
            # - if no, then proceed as normally: clear the field
            for field_name, value in self._mt_form_pending_clear.items():
                field = self._meta.get_field(field_name)
                orig_field_name = field.translated_field.name
                if orig_field_name in exclude:
                    field.save_form_data(self, value, check=False)
            delattr(self, '_mt_form_pending_clear')
        old_clean_fields(self, exclude)
    model.clean_fields = new_clean_fields

def patch_metaclass(model):
    """
    Monkey patches original model metaclass to exclude translated fields on deferred subclasses.
    """
    old_mcs = model.__class__

    class translation_deferred_mcs(old_mcs):
        """
        This metaclass is essential for deferred subclasses (obtained via only/defer) to work.

        When deferred subclass is created, some translated fields descriptors could be overridden
        by DeferredAttribute - which would cause translation retrieval to fail.
        Prevent this from happening with deleting those attributes from class being created.
        This metaclass would be called from django.db.models.query_utils.deferred_class_factory
        """
        def __new__(cls, name, bases, attrs):
            if attrs.get('_deferred', False):
                opts = translator.get_options_for_model(model)
                for field_name in opts.fields.keys():
                    attrs.pop(field_name, None)
            return super(translation_deferred_mcs, cls).__new__(cls, name, bases, attrs)
    # Assign to __metaclass__ wouldn't work, since metaclass search algorithm check for __class__.
    # http://docs.python.org/2/reference/datamodel.html#__metaclass__
    model.__class__ = translation_deferred_mcs


def delete_cache_fields(model):
    opts = model._meta
    cached_attrs = ('_field_cache', '_field_name_cache', '_name_map', 'fields', 'concrete_fields',
                    'local_concrete_fields')
    for attr in cached_attrs:
        try:
            delattr(opts, attr)
        except AttributeError:
            pass


# inspired from modeltranslations.fields.TranslationFieldDescriptor
class OriginalFieldDescriptor(object):
    def __init__(self, field):
        self.field = field


# inspired from modeltranslations.fields.TranslationFieldDescriptor
class GettextFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __set__(self, instance, value):
        if getattr(instance, '_mt_init', False):
            return
        setattr(instance, '_%s' % self.field.name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        val = getattr(instance, '_%s' % self.field.name, None)
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
        # Ensure that a base is not registered after a subclass (_registry
        # is closed with respect to taking bases, so we can just check if
        # we've seen the model).
        if model in self._registry:
            if self._registry[model].registered:
                raise AlreadyRegistered(
                    'Model "%s" is already registered for translation' %
                    model.__name__)
            else:
                descendants = [d.__name__ for d in self._registry.keys()
                               if issubclass(d, model) and d != model]
                raise DescendantRegistered(
                    'Model "%s" cannot be registered after its subclass'
                    ' "%s"' % (model.__name__, descendants[0]))


        opts = self._get_options_for_model(model, opts_class, **options)
        opts.registered = True
        # Delete all fields cache for related model (parent and children)
        for related_obj in model._meta.get_all_related_objects():
            delete_cache_fields(related_obj.model)

        # Connect signal for model
        post_init.connect(delete_mt_init, sender=model)


        patch_clean_fields(model)
        patch_metaclass(model)

        for field_name in opts.local_fields.keys():
            ref_field_name = "ref_{field}".format(field=field_name)

            field = model._meta.get_field(field_name)

            ref_descriptor = OriginalFieldDescriptor(field)
            descriptor = GettextFieldDescriptor(field)

            setattr(model, field_name, descriptor)
            setattr(model, ref_field_name, ref_descriptor)

            opts.add_translation_field(field_name, descriptor)
            opts.add_translation_field(field_name, ref_descriptor)


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
        return [(model, opts) for (model, opts) in self._registry.items()
                if getattr(opts, 'registered', False) and (not model._meta.abstract or abstract)]

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

    def get_options_for_model(self, model):
        """
        Thin wrapper around ``_get_options_for_model`` to preserve the
        semantic of throwing exception for models not directly registered.
        """
        opts = self._get_options_for_model(model)
        if not getattr(opts, 'registered', False) and not getattr(opts, 'related', False):
            raise NotRegistered('The model "%s" is not registered for '
                                'translation' % model.__class__.__name__)
        return opts

translator = Translator()