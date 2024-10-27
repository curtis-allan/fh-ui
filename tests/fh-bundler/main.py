from fasthtml.common import *
from src import FastHTMLBundler, BundleConfig, bundled_script, bundled_style, DevServer

app, rt = fast_app()

DEBUG = True

config = BundleConfig(
    entry_dir=Path("assets"),
    output_dir=Path("static/dist"),
    watch=True,
    dev_mode=True,
    minify=not DEBUG,
    sourcemaps=True,
)

bundler = FastHTMLBundler(app, config)
dev_server = DevServer(bundler)


@rt("/")
def get():
    return Titled(
        "My App",
        bundled_style("/assets/styles/main.css"),
        bundled_script("/assets/js/app.js"),
        Div(H1("Welcome"), P("Content here"), cls="container"),
    )


async def startup():
    await bundler.setup()
    if config.dev_mode:
        asyncio.create_task(dev_server.start())


if __name__ == "__main__":
    import uvicorn

    app.add_event_handler("startup", startup)
    uvicorn.run(app, host="0.0.0.0", port=8000)
