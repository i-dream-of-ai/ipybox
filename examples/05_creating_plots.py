"""
Example demonstrating how to create and save matplotlib plots.
"""

import asyncio

from gradion.executor import ExecutionClient, ExecutionContainer


async def main():
    async with ExecutionContainer() as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            execution = await client.submit("""
                !pip install matplotlib

                import matplotlib.pyplot as plt
                import numpy as np

                x = np.linspace(0, 10, 100)
                plt.figure(figsize=(8, 6))
                plt.plot(x, np.sin(x))
                plt.title('Sine Wave')
                plt.show()

                print("Plot generation complete!")
                """)

            # Stream the output text as it's generated
            print("Installation and plot generation progress:")
            async for chunk in execution.stream():
                print(chunk, end="", flush=True)

            # Obtain the execution result
            result = await execution.result()
            assert "Plot generation complete!" in result.text

            # Save the created plot
            if result.images:
                output_path = "sine_wave.png"
                result.images[0].save(output_path)
                print(f"\nPlot saved to: {output_path}")
            else:
                print("\nNo images were generated")


if __name__ == "__main__":
    asyncio.run(main())
