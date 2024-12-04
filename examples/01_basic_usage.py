"""
Basic usage example demonstrating how to execute Python code in an execution container.
"""

import asyncio

from gradion.executor import ExecutionClient, ExecutionContainer


async def main():
    # Create and start a container for code execution
    async with ExecutionContainer(tag="gradion/executor") as container:
        # Create and connect to an IPython kernel
        async with ExecutionClient(host="localhost", port=container.port) as client:
            # Execute Python code and await the result
            result = await client.execute("print('Hello, world!')")
            # Print the execution output text
            print(f"Output: {result.text}")  # Output: Hello, world!


if __name__ == "__main__":
    asyncio.run(main())
