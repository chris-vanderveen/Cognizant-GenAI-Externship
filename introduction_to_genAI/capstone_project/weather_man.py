from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Vertical
from textual.css.query import QueryType
from textual.widgets import (
    Footer,
    Header,
    Rule,
    MarkdownViewer,
    LoadingIndicator,
    Label,
    Button,
    Input,
)

class WeatherMan(App):
    """A Textual app to interact with a WeatherMan Agent"""

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()
        yield QueryInput()

class QueryInput(HorizontalGroup):
    """A widget to get text input from the user"""

    def compose(self) -> ComposeResult:
        """Create child widgets of a QueryInput"""
        yield Input(placeholder="Enter a US location to get the weather!")
        yield Button("Go!", id="submit", variant="primary")

if __name__ == "__main__":
    app = WeatherMan()
    app.run()
