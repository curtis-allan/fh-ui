from fasthtml.common import *
import os

from core import React


DEV_MODE = os.getenv("DEV_MODE", "False").lower() == "false"

script_src = (
    "http://localhost:5173/@vite/client" if DEV_MODE else "/static/react-components.js"
)
vite_client = (
    Script(src="http://localhost:5173/src/main.tsx", type="module")
    if DEV_MODE
    else None
)

vite_src = Script(
    """
import RefreshRuntime from "http://localhost:5173/@react-refresh";

RefreshRuntime.injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;
window.__vite_plugin_react_preamble_installed__ = true;""",
    type="module",
)

app, rt = fast_app(
    pico=False,
    hdrs=[vite_src, Script(src=script_src, type="module"), vite_client],
)


def MobileBar():
    return React(
        "Button",
        "Click me",
        id="name",
        type="button",
        onclick="console.log('clicked!')",
        className="bg-pink-300",
    )


@rt("/")
def get():
    return (
        Title("Vite Test"),
        Main("Welcome!", MobileBar()),
    )


serve()
