from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack
from dataclasses import dataclass

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
MODEL = "claude-3-7-sonnet-20250219"

@dataclass
class ClientResponse:
    """Structured response from the MCP client"""
    success: bool
    content: str
    error: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self):
        if self.tool_calls is None:
            self.tool_calls = []

@dataclass
class ToolInfo:
    """Information about available tools"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class WeatherMCPClient:
    """MCP client interface for weather operations with conversation memory"""
    def __init__(self, max_context_messages: int = 20):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self._connected = False
        self._available_tools: List[ToolInfo] = []

        # Conversation memory
        self.conversation_history: List[Dict[str, str]] = []
        self.max_context_messages = max_context_messages

        # System prompt
        self.system_prompt = ("You are a helpful assistant with access to weather tools. "
                             "You can have conversations, answer questions on any topic, and use weather tools when appropriate. "
                             "Be conversational and remember previous parts of our conversation.")

    @property
    def is_connected(self) -> bool:
        """Check if client is connected to MCP server"""
        return self._connected and self.session is not None

    def add_to_conversation(self, role: str, content: str):
        """Add a message to conversation history"""
        if role in ["user", "assistant"]:
            self.conversation_history.append({"role": role, "content": content})

            # Keep only the last N messages to prevent context overflow
            if len(self.conversation_history) > self.max_context_messages:
                self.conversation_history = self.conversation_history[-self.max_context_messages:]

    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    async def connect(self, server_script_path: str = "weather.py") -> ClientResponse:
        """Connect to weather MCP server

        Args:
            server_script_path: Path to the server script

        Returns:
            ClientResponse indicating success/failure
        """
        try:
            server_params = StdioServerParameters(
                command="python",
                args=[server_script_path],
                env=None
            )

            # Create the transport and session
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.stdio, self.write)
            )

            await self.session.initialize()

            # Get available tools
            response = await self.session.list_tools()
            self._available_tools = [
                ToolInfo(
                    name=tool.name,
                    description=tool.description or "",
                    input_schema=tool.inputSchema
                )
                for tool in response.tools
            ]

            self._connected = True

            tool_names = [tool.name for tool in self._available_tools]

            return ClientResponse(
                success=True,
                content=f"Connected successfully. Available tools: {', '.join(tool_names)}"
            )

        except Exception as e:
            self._connected = False
            return ClientResponse(
                success=False,
                content="",
                error=f"Failed to connect to server: {str(e)}"
            )

    async def get_available_tools(self) -> List[ToolInfo]:
        """Get list of tools"""
        return self._available_tools.copy()

    async def process_query(self, query: str) -> ClientResponse:
        """Process a query using Claude and available tools with conversation context

        Args:
            query: User query to process

        Returns:
            ClientResponse with the result
        """
        if not self.is_connected:
            return ClientResponse(
                success=False,
                content="",
                error="Not connected to MCP server"
            )

        try:
            # Add user message to conversation history
            self.add_to_conversation("user", query)

            # Build messages with conversation context (user/assistant only)
            messages = self.conversation_history.copy()

            # Prep tools for Claude
            available_tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            } for tool in self._available_tools]

            # FIXED: Pass system prompt as separate parameter
            response = self.anthropic.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=self.system_prompt,
                messages=messages,
                tools=available_tools
            )

            # Process response and handle tool calls
            tool_calls_made = []
            final_text = []

            # Check if there are tool calls to handle
            tool_use_blocks = [content for content in response.content if content.type == 'tool_use']

            if tool_use_blocks:
                # Add the assistant's response with tool calls
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Executetool calls and collect results
                tool_results = []
                for content in response.content:
                    if content.type == 'tool_use':
                        tool_name = content.name
                        tool_args = content.input
                        tool_id = content.id

                        # Execute tool call via MCP
                        result = await self.session.call_tool(tool_name, tool_args)

                        tool_calls_made.append({
                            "tool": tool_name,
                            "args": tool_args,
                            "result": result.content[0].text if result.content else "No result"
                        })

                        # Add tool result
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result.content[0].text if result.content else "No result"
                        })

                # Add tool results message
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                # Get Claude's final response after tool execution
                final_response = self.anthropic.messages.create(
                    model=MODEL,
                    max_tokens=1000,
                    system=self.system_prompt,  # System prompt here too
                    messages=messages,
                )

                # Extract text from final response
                for content in final_response.content:
                    if content.type == 'text':
                        final_text.append(content.text)
            else:
                # No tool calls, just extract text
                for content in response.content:
                    if content.type == 'text':
                        final_text.append(content.text)

            assistant_response = "\n".join(final_text) if final_text else "No response generated"

            # Add assistant response to conversation history
            self.add_to_conversation("assistant", assistant_response)

            return ClientResponse(
                success=True,
                content=assistant_response,
                tool_calls=tool_calls_made
            )

        except Exception as e:
            return ClientResponse(
                success=False,
                content="",
                error=f"Error processing query: {str(e)}"
            )

    async def cleanup(self):
        """Clean up resources"""
        try:
            await self.exit_stack.aclose()
        except Exception:
            pass
        finally:
            self._connected = False
            self._available_tools = []
            self.conversation_history = []

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
