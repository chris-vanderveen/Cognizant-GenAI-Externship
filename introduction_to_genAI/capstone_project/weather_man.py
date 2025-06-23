from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Vertical, ScrollableContainer
from textual.widgets import (
    Footer,
    Header,
    LoadingIndicator,
    Button,
    Input,
    Static,
)
from textual.message import Message
import asyncio
from datetime import datetime
from typing import Optional

from client import WeatherMCPClient

class ChatBubble(Static):
    """A chat bubble widget for messages"""

    def __init__(self, content: str, is_user: bool = False, timestamp: str = None):
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now().strftime("%H:%M")
        self.loading_indicator: Optional[LoadingIndicator] = None

        # Add timestamp to content
        formatted_content = f"{content}\n[dim]{self.timestamp}[/dim]"

        # Set classes based on message type
        classes = "user-bubble" if is_user else "assistant-bubble"
        super().__init__(formatted_content, classes=classes)

    def show_loading(self):
        """Show loading indicator inside this bubble"""
        if not self.loading_indicator:
            self.loading_indicator = LoadingIndicator()
            self.mount(self.loading_indicator)

    def hide_loading_and_set_content(self, content: str):
        """Hide loading and update with final content"""
        if self.loading_indicator:
            self.loading_indicator.remove()
            self.loading_indicator = None

        # Update with final content and timestamp
        formatted_content = f"{content}\n[dim]{self.timestamp}[/dim]"
        self.update(formatted_content)


class ChatArea(ScrollableContainer):
    """Scrollable chat area containing all messages"""

    def __init__(self):
        super().__init__(id="chat-area")
        self.current_assistant_bubble: Optional[ChatBubble] = None

    def add_user_message(self, content: str):
        """Add a user message bubble"""
        bubble = ChatBubble(content, is_user=True)
        self.mount(bubble)
        self.call_after_refresh(lambda: self.scroll_end(animate=True))
        return bubble

    def add_assistant_message(self, content: str):
        """Add an assistant message bubble"""
        bubble = ChatBubble(content, is_user=False)
        self.mount(bubble)
        self.call_after_refresh(lambda: self.scroll_end(animate=True))
        return bubble

    def start_assistant_response(self):
        """Start a new assistant response with loading indicator"""
        # Create assistant bubble with loading
        self.current_assistant_bubble = ChatBubble("", is_user=False)
        self.mount(self.current_assistant_bubble)
        self.current_assistant_bubble.show_loading()
        self.call_after_refresh(lambda: self.scroll_end(animate=True))
        return self.current_assistant_bubble

    def finish_assistant_response(self, content: str):
        """Finish the assistant response by replacing loading with content"""
        if self.current_assistant_bubble:
            self.current_assistant_bubble.hide_loading_and_set_content(content)
            self.current_assistant_bubble = None
        else:
            # Fallback: create new bubble
            self.add_assistant_message(content)


class QueryInput(HorizontalGroup):
    """A widget to get txet input from the user"""

    def compose(self) -> ComposeResult:
        """Create child widgets of a QueryInput"""
        yield Input(
            placeholder="Ask about weather or anything else...",
            id="user-input"
        )
        yield Button("Send", id="submit", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "submit":
            # Get the input value and send it to parent
            user_input = self.query_one("#user-input", Input)
            if user_input.value.strip():
                # Post a custom message to the app
                self.post_message(self.SubmitQuery(user_input.value))
                user_input.value = ""

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission via Enter key"""
        if event.value.strip():
            # Post custom message to the app
            self.post_message(self.SubmitQuery(event.value))
            event.input.value = ""

    class SubmitQuery(Message):
        """Custom message for query submission"""
        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()


class WeatherMan(App):
    """A Textual app to interact with a WeatherMan Agent"""

    CSS = """
    /* Main layout */
    #chat-container {
        height: 1fr;
        border: round $primary;
        margin: 1;
    }

    #chat-area {
        height: 1fr;
        padding: 1;
    }

    /* Input area */
    QueryInput {
        dock: bottom;
        height: 3;
        margin: 1 1 2 1;
    }

    #user-input {
        width: 1fr;
        margin-right: 1;
    }

    #submit {
        width: 12;
        min-width: 12;
        margin-right: 2;
    }

    /* Chat bubbles */
    .user-bubble {
        max-width: 99%;
        padding: 1 2;
        border: round $primary;
        background: transparent;
        color: $text;
        content-align: right middle;
    }

    .assistant-bubble {
        max-width: 99%;
        padding: 1 2;
        border: round $accent;
        background: transparent;
        color: $text;
        content-align: left middle;
    }

    LoadingIndicator {
        width: auto;
        height: auto;
        margin: 1;
    }
    """
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_conversation", "Clear Chat"),
    ]

    def __init__(self):
        super().__init__()
        self.client = WeatherMCPClient()
        self.connected = False
        self.processing = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()

        # Main chat container
        with Vertical(id="chat-container"):
            yield ChatArea()

        # Input at bottom
        yield QueryInput()

        yield Footer()

    async def on_mount(self) -> None:
        """Initialize the app"""
        chat_area = self.query_one(ChatArea)
        chat_area.add_assistant_message("Welcome to WeatherMan Weather Assistant! I am an Agentic AI assistant with access to tools that allow me to get live weather for US cities.")
        chat_area.add_assistant_message("Connecting to weather server...")

        # Connect to weather server
        await self.connect_weather_server()

    async def connect_weather_server(self):
        """Connect to the weather MCP server"""
        chat_area = self.query_one(ChatArea)

        try:
            response = await self.client.connect("weather.py")

            if response.success:
                self.connected = True
                chat_area.add_assistant_message("Connected! You can now ask weather questions or chat about anything.")

            else:
                chat_area.add_assistant_message(f" Weather tools unavailable: {response.error}")

        except Exception as e:
            chat_area.add_assistant_message(f" Starting without weather tools: {str(e)}")

        # Focus the input
        self.query_one("#user-input", Input).focus()

    def on_query_input_submit_query(self, event: QueryInput.SubmitQuery) -> None:
        """Handle query submission from the input widget"""
        # Run the async process_query in a task
        asyncio.create_task(self.process_query(event.query))

    async def process_query(self, query: str):
        """Process user query and show response"""
        query = query.strip()
        if not query or self.processing:
            return

        self.processing = True
        chat_area = self.query_one(ChatArea)

        # Add user message
        chat_area.add_user_message(query)

        # Show loading indicator
        chat_area.start_assistant_response()

        try:
            if self.connected:
                # Use MCP client for weather + general chat
                response = await self.client.process_query(query)

                if response.success:
                    # Add assistant response (left side)
                    chat_area.finish_assistant_response(response.content)

                else:
                    chat_area.finish_assistant_response(f"Error: {response.error}")
            else:
                # Fallback to basic response without weather tools
                chat_area.finish_assistant_response(
                    "I don't have access to weather tools right now, but I'm here to chat! "
                    "Try asking me about other topics or general questions."
                )

        except Exception as e:
            chat_area.finish_assistant_response(f"Error: {str(e)}")
        finally:
            self.processing = False

    def action_clear_conversation(self) -> None:
        """Clear the conversation history and chat area"""
        # Clear the client's conversation memory
        if hasattr(self.client, 'clear_conversation'):
            self.client.clear_conversation()

        # Clear the chat area
        chat_area = self.query_one(ChatArea)
        # Remove all children
        for child in list(chat_area.children):
            child.remove()

        # Add welcome message
        chat_area.add_assistant_message("Conversation cleared! How can I help you?")

    async def on_unmount(self):
        """Clean up when app closes"""
        if hasattr(self, 'client'):
            await self.client.cleanup()


if __name__ == "__main__":
    app = WeatherMan()
    app.run()
