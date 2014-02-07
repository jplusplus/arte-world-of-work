import re

def find(iterator, iterable):
    """
    Return the first element wich return true by applying iterator to iterable.
    Return None if no element has been found.
    """
    for el in iterable:
        if iterator(el):
            return el
    return None


def find_modelinstance(obj, iterable):
    _l = lambda e: obj.id == e.id
    return find(_l, iterable)


def db_table_exists(table_name):
    # took from https://gist.github.com/rctay/527113#comment-337110
    from django.db import connection
    return table_name in connection.introspection.table_names()


def get_subclasses(classes, level=0):
    """
        Return the list of all subclasses given class (or list of classes) has.
        Inspired by this question:
        http://stackoverflow.com/questions/3862310/how-can-i-find-all-subclasses-of-a-given-class-in-python
    """
    # for convenience, only one class can can be accepted as argument
    # converting to list if this is the case
    if not isinstance(classes, list):
        classes = [classes]

    if level < len(classes):
        classes += classes[level].__subclasses__()
        return get_subclasses(classes, level+1)
    else:
        return classes

def receiver_subclasses(signal, sender, dispatch_uid_prefix, **kwargs):
    import logging
    """
    A decorator for connecting receivers and all receiver's subclasses to signals. Used by passing in the
    signal and keyword arguments to connect::

        @receiver_subclasses(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...
    """
    def _decorator(func):
        all_senders = get_subclasses(sender)
        logging.info(all_senders)
        for snd in all_senders:
            signal.connect(func, sender=snd, dispatch_uid=dispatch_uid_prefix+'_'+snd.__name__, **kwargs)
        return func
    return _decorator


def get_fields_names(model=None, type=None):
    names = []
    if type != None and model != None:
        for field in model._meta.fields:
            if isinstance(field, type):
                names.append(field.name)
    return names



def camel_to_underscore(str):
    # took from http://stackoverflow.com/a/1176023/885541
    _str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', _str).lower()


class TestCaseMixin():
    # ------------------------------------------------------------------------- 
    # Utility methods for test case
    # ------------------------------------------------------------------------- 
    def assertLenIs(self, enum, size):
        # check the passed `enum` has the appropriated length 
        self.assertEqual(len(enum), size)

    def assertModelIn(self, enum, model_instance):
        # check the element with `pk` is in `enum`
        self.assertIsNotNone(self.findElement(enum, model_instance.pk))

    def assertAttrNotNone(self, elem, attr):
        self.assertIsNotNone(elem.get(attr, None))

    def debug(self, msg):
        print "\n[DBG - {time}] {msg}".format(time=datetime.now(), msg=msg)

    def createModelInstance(self, klass, **kwargs):
        elem = klass.objects.create(**kwargs)
        elem.save()
        return elem
