from typing import Union, List, Dict, Any
import json

__all__ = ["React"]


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_event_handler(attr: str, value: str) -> str:
    if attr.startswith("on"):
        # Convert onclick="console.log('test')" to onClick={() => console.log('test')}
        return f"{to_camel_case(attr)}={{() => {value}}}"
    return f'{attr}="{value}"'


def ft2jsx(
    component: Union[str, callable], *children: List[Any], **attrs: Dict[str, Any]
) -> str:
    tag_name = component if isinstance(component, str) else component.__name__

    # Convert attributes
    converted_attrs = []
    for attr, value in attrs.items():
        if attr == "cls":
            converted_attrs.append(f'className="{value}"')
        elif attr.startswith("on"):
            converted_attrs.append(convert_event_handler(attr, value))
        else:
            converted_attrs.append(f'{attr}="{value}"')

    attr_string = " ".join(converted_attrs)

    # Convert children
    child_jsx = []
    for child in children:
        if isinstance(child, str):
            child_jsx.append(child)
        elif callable(child):
            child_jsx.append(ft2jsx(child))
        else:
            child_jsx.append(str(child))

    children_string = "".join(child_jsx)

    # Render JSX
    if children_string:
        return f"<{tag_name} {attr_string}>{children_string}</{tag_name}>"
    else:
        return f"<{tag_name} {attr_string} />"


def React(tag: str, *c, **kwargs):
    from fasthtml.components import Div

    return Div(
        *c,
        data_tag=tag,
        data_attrs=json.dumps(kwargs),
        cls="react-component",
    )
