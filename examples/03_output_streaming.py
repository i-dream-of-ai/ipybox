"""
Example demonstrating output streaming during code execution.
"""

import asyncio

from ipybox import ExecutionClient, ExecutionContainer


async def main():
    async with ExecutionContainer() as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            # Code that produces output gradually
            code = """
            import time
            for i in range(5):
                print(f"Processing step {i}")
                time.sleep(1)
            """

            # Submit the execution and stream the output
            execution = await client.submit(code)
            print("Streaming output:")
            async for chunk in execution.stream():
                print(f"Received output: {chunk.strip()}")

            # Get the aggregated output as a single result
            result = await execution.result()
            print("\nAggregated output:")
            print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
