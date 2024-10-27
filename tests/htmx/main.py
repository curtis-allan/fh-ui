from fasthtml.common import *

htmx_hdrs = [
    Script(
        src="https://unpkg.com/htmx.org@2.0.3",
        integrity="sha384-0895/pl2MU10Hqc6jd4RvrthNlDiE9U1tWmX7WRESftEDRosgxNsQG/Ze9YMRzHq",
        crossorigin="anonymous",
    ),
    Script(
        src="https://unpkg.com/idiomorph@0.3.0/dist/idiomorph-ext.min.js",
        _async=True,
        defer=True,
    ),
    Script(
        src="https://unpkg.com/htmx-ext-preload@2.0.1/preload.js",
        _async=True,
        defer=True,
    ),
]

app, rt = fast_app(
    default_hdrs=False,
    live=True,
    hdrs=[*htmx_hdrs, Stript(src="https://cdn.tailwindcss.com")],
)


@rt("/")
def get():
    return (Title("Testing"), Main(H1("Test"), Div(Button)))
