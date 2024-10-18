from fasthtml.common import *

babel = Script(src="https://unpkg.com/@babel/standalone/babel.min.js")

js = Script(crossorigin=True, src="/dist/assets/index-C2w5Il63.js", type="module")

css = Link(crossorigin=True, rel="stylesheet", href="/dist/assets/index-DuxjBh9a.css")

app, rt = fast_app(pico=False, live=True, hdrs=[js, css])


@rt("/")
def get():
    return Titled(
        "Welcome",
        Div(id="root"),
    )


@rt("/button")
def get():
    return


serve()


def MyButton(*c, **kwargs):
    return Div(id="root")
