from dataclasses import dataclass
from fasthtml.common import *
import json


@dataclass
class ChakraComponent:
    """Base class for Chakra UI components"""

    def _props_to_json(self, **kwargs):
        return json.dumps({k: v for k, v in kwargs.items() if k not in ["cls", "id"]})


class Button(ChakraComponent):
    def __call__(self, text, **kwargs):
        return Div(
            text,
            data_component="ChakraButton",
            data_props=self._props_to_json(**kwargs),
            cls=f"chakra-button {kwargs.get('cls', '')}",
        )


class Input(ChakraComponent):
    def __call__(self, **kwargs):
        return Div(
            data_component="ChakraInput",
            data_props=self._props_to_json(**kwargs),
            cls=f"chakra-input {kwargs.get('cls', '')}",
        )


def chakra_headers():
    return (
        Script(
            src="https://cdn.jsdelivr.net/npm/chakra-ui/dist/index.min.js", defer=True
        ),
        Script(
            """
            import React from 'https://esm.sh/react';
            import {createRoot} from 'https://esm.sh/react-dom/client';
            
            function hydrateComponent(el) {
                const name = el.dataset.component;
                const props = JSON.parse(el.dataset.props || '{}');
                
                console.log(window);
               
                const root = createRoot(el);

                root.render(React.createElement('span', {...props}, el.innerHTML));
            }

            window.addEventListener('DOMContentLoaded', () => {
                document.querySelectorAll('[data-component]').forEach(hydrateComponent);
            });
        """,
            type="module",
        ),
    )
