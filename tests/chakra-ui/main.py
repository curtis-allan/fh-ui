from fasthtml.common import *
from components.chakra import Button, Input, chakra_headers

# Initialize components
ChakraButton = Button()
ChakraInput = Input()

# Create FastHTML app with Chakra headers
app, rt = fast_app(hdrs=chakra_headers())


@rt("/")
def get():
    return Titled(
        "Chakra UI Demo",
        ChakraButton("Primary Button", colorScheme="blue", size="lg"),
        ChakraButton("Ghost Button", colorScheme="teal", variant="ghost"),
        ChakraInput(placeholder="Enter text...", size="lg"),
        direction="column",
        spacing="4",
    )


serve()
