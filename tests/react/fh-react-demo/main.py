from fasthtml.common import *
from typing import Any, Dict
from dataclasses import dataclass, field
import json


@dataclass
class ReactIsland:
    """React island component for FastHTML"""

    children: Any
    bindings: Dict[str, Any] = field(default_factory=dict)
    component: str = "Island"
    hydrate: bool = True

    def ft_to_jsx(self, ft) -> str:
        """Convert FT components to JSX string"""
        # Handle primitive types
        if isinstance(ft, (str, int, float, bool)):
            return str(ft)

        # Handle FT structure
        if not isinstance(ft, (list, tuple)) or len(ft) != 3:
            return str(ft)

        tag, children, attrs = ft

        # Convert FastHTML attributes to React props
        props_str = ""
        if attrs is not None:
            props = []
            for k, v in attrs.items():
                if k == "cls":
                    props.append(f'className="{v}"')
                elif k.startswith("on_"):
                    event = k[3:].capitalize()
                    props.append(f"on{event}={v}")
                else:
                    if isinstance(v, (str, int, float, bool)):
                        props.append(f'{k}="{v}"')
                    else:
                        props.append(f"{k}={{{json.dumps(v)}}}")
            props_str = " ".join(props)

        # Process children
        if isinstance(children, (list, tuple)):
            children_str = "".join(self.ft_to_jsx(child) for child in children)
        else:
            children_str = self.ft_to_jsx(children) if children is not None else ""

        return f"<{tag} {props_str}>{children_str}</{tag}>"

    def __ft__(self):
        try:
            jsx = self.ft_to_jsx(self.children)
            return Div(
                NotStr(jsx),
                id=f"island-{id(self)}",
                data_component=self.component,
                data_bindings=json.dumps(self.bindings),
                data_hydrate=str(self.hydrate).lower(),
                cls="react-island",
            )
        except Exception as e:
            print(f"Error in ReactIsland.__ft__: {e}")
            raise


static_head = [
    Script(
        """import RefreshRuntime from 'http://localhost:5173/@react-refresh'
  RefreshRuntime.injectIntoGlobalHook(window)
  window.$RefreshReg$ = () => {}
  window.$RefreshSig$ = () => (type) => type
  window.__vite_plugin_react_preamble_installed__ = true""",
        type="module",
    ),
    Script(src="http://localhost:5173/@vite/client", type="module", crossorigin=True),
    Script(src="http://localhost:5173/client.tsx", type="module", crossorigin=True),
]

# Initialize app
app, rt = fast_app(pico=False, hdrs=[*static_head], live=True)

app.static_route_exts("/frontend/src")


@rt("/")
def get():
    return Main(
        ReactIsland(
            Div(
                H1("React Components Demo", cls="title"),
                Button(
                    "Click me", variant="outline", on_click="() => alert('Clicked!')"
                ),
                Input(
                    placeholder="Type something...",
                    on_change="(e) => console.log(e.target.value)",
                ),
            )
        )
    )


serve()
