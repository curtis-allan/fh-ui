from fasthtml.common import *

tw_cdn = Script(src="https://cdn.tailwindcss.com")

app, rt = fast_app(pico=False, live=True, hdrs=[tw_cdn])


@rt("/")
def get():
    return Titled("Welcome", Container(H2("Experiments")))


serve()


def MyButton(*c, **kwargs):
    return Script()
