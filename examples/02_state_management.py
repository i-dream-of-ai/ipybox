"""
Example demonstrating state management between different client contexts.
"""

import asyncio

from ipybox import ExecutionClient, ExecutionContainer, ExecutionError


async def main():
    async with ExecutionContainer() as container:
        # First client context
        async with ExecutionClient(host="localhost", port=container.port) as client_1:
            # Execute code that defines variable x
            result = await client_1.execute("x = 1")
            assert result.text is None

            # Reference variable x defined in previous execution
            result = await client_1.execute("print(x)")
            assert result.text == "1"
            print("Client 1 successfully accessed variable x")

        # Second client context
        async with ExecutionClient(host="localhost", port=container.port) as client_2:
            # Variable x is not defined in this client context
            try:
                await client_2.execute("print(x)")
            except ExecutionError as e:
                print(f"Client 2 error (expected): {e.args[0]}")
                assert e.args[0] == "NameError: name 'x' is not defined"


if __name__ == "__main__":
    asyncio.run(main())
