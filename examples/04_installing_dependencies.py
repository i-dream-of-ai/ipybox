"""
Example demonstrating how to install dependencies at runtime.
"""

import asyncio

from gradion.executor import ExecutionClient, ExecutionContainer


async def main():
    async with ExecutionContainer() as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            print("Installing einops package...")
            # Install the einops package
            await client.execute("!pip install einops")

            # Then you can use it in the following code execution
            result = await client.execute("""
                import einops
                print(einops.__version__)
            """)
            print(f"Output: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
