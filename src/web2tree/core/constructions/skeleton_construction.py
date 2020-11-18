from web2tree import DIV
from web2tree.utils.data_wrangling import wrap_attr


def wrap_into_div(to_be_wrapped):
    return construct_skeleton(DIV, content=to_be_wrapped)


def construct_skeleton(element_type, **attrs):
    content = attrs.pop("content", None)
    attrs = " ".join(
        (
            "{attr_k}={attr_v}".format(
                attr_k=str(attr_k), attr_v=wrap_attr(attrs[attr_k])
            )
            for attr_k in attrs.keys()
        )
    )
    if attrs == "":
        gap = ""
    else:
        gap = " "
    if content is None:
        return "<{type}{gap}{attrs}/>".format(
            type=element_type,
            gap=gap,
            attrs=attrs,
        )
    else:
        return "<{type}{gap}{attrs}>{content}</{type}>".format(
            type=element_type, gap=gap, content=content, attrs=attrs
        )
