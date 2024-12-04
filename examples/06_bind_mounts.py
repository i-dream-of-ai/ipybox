"""
Example demonstrating how to use bind mounts to access host files.
"""

import asyncio
import os

import aiofiles


async def main():
    # Create data and output directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Map host paths to container paths
    binds = {
        "./data": "data",  # Read data from host
        "./output": "output",  # Write results to host
    }

    # Create a data file on the host
    async with aiofiles.open("data/input.txt", "w") as f:
        await f.write("hello world")

    from gradion.executor import ExecutionClient, ExecutionContainer

    async with ExecutionContainer(binds=binds) as container:  # type: ignore
        async with ExecutionClient(host="localhost", port=container.port) as client:
            # Read from mounted data directory and write to output directory
            result = await client.execute("""
                # Read from mounted data directory
                with open('data/input.txt') as f:
                    data = f.read()

                # Process data
                processed = data.upper()

                # Write to mounted output directory
                with open('output/result.txt', 'w') as f:
                    f.write(processed)

                print(f"Input data: {data}")
                print(f"Processed data: {processed}")
            """)
            print("\nExecution output:")
            print(result.text)

    # Check the result file on the host
    async with aiofiles.open("output/result.txt", "r") as f:
        result = await f.read()
        print(f"\nContent of output/result.txt: {result}")
        assert result == "HELLO WORLD"


if __name__ == "__main__":
    asyncio.run(main())
