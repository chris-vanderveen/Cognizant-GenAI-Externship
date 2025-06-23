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
    """MCP client interface for weather operations"""
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self._connected = False
        self._available_tools: List[ToolInfo] = []

    @property
    def is_connected(self) -> bool:
        """Check if client is connected to MCP server"""
        return self._connected and self.session is not None

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
        """Process a query using Claude and available tools

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
            messages = [{"role": "user", "content": query}]

            # Prep tools for Claude
            available_tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            } for tool in self._available_tools]

            response = self.anthropic.messages.create(
                model=MODEL,
                max_tokens=1000,
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

                # Execute all tool calls and collect results
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

            content = "\n".join(final_text) if final_text else "No response generated"

            return ClientResponse(
                success=True,
                content=content,
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

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
