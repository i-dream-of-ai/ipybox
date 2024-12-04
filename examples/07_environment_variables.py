"""
Example demonstrating how to use environment variables in the execution container.
"""

import asyncio

from gradion.executor import ExecutionClient, ExecutionContainer


async def main():
    # Define environment variables for the container
    env = {"API_KEY": "secret-key-123", "DEBUG": "1"}

    async with ExecutionContainer(env=env) as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            # Access environment variables in executed code
            result = await client.execute("""
                import os

                api_key = os.environ['API_KEY']
                print(f"Using API key: {api_key}")

                debug = bool(int(os.environ.get('DEBUG', '0')))
                if debug:
                    print("Debug mode enabled")
            """)
            print("Execution output:")
            print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
