from web2tree.utils.data_wrangling import wrap_attr


class Element:
    def __init__(self, type):
        self.type = type

    def to_skeleton(self, **attrs):
        content = attrs.pop("content", None)
        if content is None:
            return "<{type} {attrs}/>".format(
                type=self.type,
                attrs=" ".join(
                    (
                        "{attr_k}={attr_v}".format(
                            attr_k=str(attr_k), attr_v=wrap_attr(attrs[attr_k])
                        )
                        for attr_k in attrs.keys()
                    )
                ),
            )
