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