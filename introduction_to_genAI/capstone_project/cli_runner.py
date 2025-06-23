#!/usr/bin/env python3
"""
Command line interface for the weather MCP client
"""
import asyncio
import sys
from pathlib import Path

from client import WeatherMCPClient


async def run_cli(server_path: str = "weather.py"):
    """Run the command line interface"""
    print("🌤️  Weather MCP Client")
    print("=" * 50)

    client = WeatherMCPClient()

    try:
        # Connect to server
        print(f"Connecting to {server_path}...")
        connection_result = await client.connect(server_path)

        if not connection_result.success:
            print(f"❌ {connection_result.error}")
            return

        print(f"✅ {connection_result.content}")

        # Show available tools
        tools = await client.get_available_tools()
        print(f"\n📡 Available tools:")
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")

        print("\n💬 Start asking questions! Type 'quit' to exit.")
        print("-" * 50)

        # Interactive loop
        while True:
            try:
                query = input("\n🌤️  Query: ").strip()

                if query.lower() in ['quit', 'exit', 'q']:
                    break

                if not query:
                    continue

                print("🤔 Processing...")
                response = await client.process_query(query)

                if response.success:
                    print(f"\n🤖 Assistant:")
                    print(response.content)

                    # Show tool calls if any were made
                    if response.tool_calls:
                        print(f"\n🔧 Tools used:")
                        for call in response.tool_calls:
                            print(f"  • {call['tool']} with {call['args']}")
                else:
                    print(f"\n❌ Error: {response.error}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

    finally:
        await client.cleanup()


def main():
    """Main entry point"""
    server_path = sys.argv[1] if len(sys.argv) > 1 else "weather.py"

    try:
        asyncio.run(run_cli(server_path))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
