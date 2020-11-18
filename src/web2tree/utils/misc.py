def is_iterable(obj):
    """return True if obj is iterable"""
    try:
        iter(obj)
    except TypeError as e:
        return False
    else:
        return True


def is_char(obj):
    """return True if obj is a char (str with lenth<=1)"""
    return isinstance(obj, str) and len(obj) <= 1


def is_char_or_noniterable(x):
    return is_char(x) or not is_iterable(x)
