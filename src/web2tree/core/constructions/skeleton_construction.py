from web2tree.utils.data_wrangling import wrap_attr


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
    if content is None:
        return "<{type} {attrs}/>".format(
            type=element_type,
            attrs=attrs,
        )
    else:
        return "<{type} {attrs}>{content}</{type}>".format(
            type=element_type, content=content, attrs=attrs
        )
