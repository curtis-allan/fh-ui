from fasthtml.common import *

app, rt = fast_app(live=True)


def Reactive(tag: str = "div", **kwargs):
    id = unqid()

    imports = """
    import { createSignal } from 'https://esm.sh/solid-js@1.8.1';
    import { render } from 'https://esm.sh/solid-js@1.8.1/web';
    import h from 'https://esm.sh/solid-js@1.8.1/h'\n\n"""

    content = """const %s = () => {
         const [count, setCount] = createSignal(0);
         const incr = (e) => setCount(c => c+1);\n\n
         """ % tag.title()

    element = """return h('%s', {onClick: incr}, count);\n}\n""" % tag

    target = (
        """htmx.onLoad((content) => { 
            const el = content.querySelector('#%s');
            render(Button, el);\n
            })\n
        """
        % id
    )

    return (
        Div(id=id),
        Script(
            imports + content + element + target,
            type="module",
        ),
    )


@rt("/")
def get():
    return Titled(
        "Signals Testing",
        Div(Reactive("button", type="button")),
    )


serve()
