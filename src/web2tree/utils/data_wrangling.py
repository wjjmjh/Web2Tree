from copy import copy

from web2tree.utils.misc import is_iterable


def wrap_str(val):
    if isinstance(val, str):
        return '"{}"'.format(val)
    return "{}".format(val)


def wrap_attr(attr):
    return "".join(("{", wrap_str(attr), "}"))


def split_by_arrows(arrowed, arrow):
    return arrowed.replace(" ", "").split(arrow)


def get_val_from_nested_dict(keys, nested_dict):
    assert (
        is_iterable(keys) and len(keys) >= 1
    ), "keys should be iterable and at least having one key."

    if len(keys) == 1:
        return nested_dict[keys[0]]
    else:
        return get_val_from_nested_dict(keys[1:], nested_dict[keys[0]])


def set_val_for_nested_dict(keys, v, nested_dict):
    assert (
        is_iterable(keys) and len(keys) >= 1
    ), "keys should be iterable and at least having one key."
    if len(keys) == 1:
        nested_dict[keys[0]] = v
        return nested_dict
    else:
        nested_dict[keys[0]] = set_val_for_nested_dict(
            keys[1:], v, nested_dict[keys[0]]
        )
        return nested_dict


def extract_all_keys_from_a_dict(dict_, keys=None, base="", keys_connector="->"):
    if keys is None:
        keys = []

    def _extract(dict_, keys, base):
        for k, v in dict_.items():
            new_base = "{base}{connector}{k}".format(
                base=base, connector=keys_connector, k=k
            )
            if isinstance(v, dict):
                keys.append(new_base)
                extract_all_keys_from_a_dict(v, keys=keys, base=new_base)
            else:
                keys.append(new_base)
        return keys

    extracted = _extract(dict_, keys, base)
    return [it.split(keys_connector)[1:] for it in extracted]
