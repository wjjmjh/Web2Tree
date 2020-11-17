def wrap_str(val):
    if isinstance(val, str):
        return '"{}"'.format(val)
    return "{}".format(val)


def wrap_attr(attr):
    return "".join(("{", wrap_str(attr), "}"))
