# Usage

The following examples demonstrate how to use the [`ExecutionContainer`](api/execution_container.md) and [`ExecutionClient`](api/execution_client.md) context managers to execute Python code in an IPython environment running in a Docker container. Runnable scripts of the following code snippets are available in the [examples](https://github.com/gradion-ai/ipybox/tree/main/examples) directory.

## Basic usage

Here's a simple example that demonstrates how to execute Python code in an execution container. The `ExecutionContainer` context manager creates and starts a container for code execution, and the `ExecutionClient` context manager connects to an IPython kernel running in the container. The example below executes the code `print('Hello, world!')` and prints the output text:

```python
from ipybox import ExecutionContainer, ExecutionClient

# Create and start a container for code execution
async with ExecutionContainer(tag="gradion/ipybox") as container:
    # Create and connect to an IPython kernel
    async with ExecutionClient(host="localhost", port=container.port) as client:
        # Execute Python code and await the result
        result = await client.execute("print('Hello, world!')")
        # Print the execution output text
        print(f"Output: {result.text}")  # Output: Hello, world!
```

The default image used by `ExecutionContainer` is `gradion/ipybox`. You can specify a custom image with the `tag` argument like in `ExecutionContainer(tag="my-box:v1")`, for example.

## State management

Code execution within the same client context is stateful i.e. you can reference variables from previous executions. Code executions in different client contexts are isolated from each other:

```python
async with ExecutionContainer() as container:
    async with ExecutionClient(host="localhost", port=container.port) as client_1:
        # Execute code that defines variable x
        result = await client_1.execute("x = 1")
        assert result.text is None

        # Reference variable x defined in previous execution
        result = await client_1.execute("print(x)")
        assert result.text == "1"

    async with ExecutionClient(host="localhost", port=container.port) as client_2:
        # Variable x is not defined in this client context
        try:
            await client_2.execute("print(x)")
        except ExecutionError as e:
            assert e.args[0] == "NameError: name 'x' is not defined"
```

## Output streaming

The execution client supports streaming output as it's generated during code execution:

```python
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
        async for chunk in execution.stream():
            # Output will be printed gradually:
            print(f"Received output: {chunk}")
            # Received output: Processing step 0
            # Received output: Processing step 1
            # Received output: Processing step 2
            # Received output: Processing step 3
            # Received output: Processing step 4

        # Get the aggregated result
        result = await execution.result()
        # Print the aggregated output text
        print(f"Aggregated output:\n{result.text}")
        # Aggregated output:
        # Processing step 0
        # Processing step 1
        # Processing step 2
        # Processing step 3
        # Processing step 4
```

The `stream()` method accepts an optional `timeout` argument (defaults to 120 seconds). In case of timeout, the execution is automatically terminated by interrupting the kernel.

## Installing dependencies at runtime

```python
async with ExecutionContainer() as container:
    async with ExecutionClient(host="localhost", port=container.port) as client:
        # Install the einops package
        await client.execute("!pip install einops")
        # Then you can use it in the following code
        # execution within the same client context
        result = await client.execute("""
            import einops
            print(einops.__version__)
        """)
        print(f"Output: {result.text}")  # Output: 0.8.0
```

## Creating and returning plots

Plots created with `matplotlib` or other libraries are returned as PIL images:

```python
async with ExecutionContainer() as container:
    async with ExecutionClient(host="localhost", port=container.port) as client:
        execution = await client.submit("""
            !pip install matplotlib

            import matplotlib.pyplot as plt
            import numpy as np
            import time

            x = np.linspace(0, 10, 100)
            plt.figure(figsize=(8, 6))
            plt.plot(x, np.sin(x))
            plt.title('Sine Wave')
            plt.show()

            print("Plot generation complete!")
            """)

        # Stream the output text as it's generated
        async for chunk in execution.stream():
            print(chunk, end="", flush=True)

        # Obtain the execution result
        result = await execution.result()
        assert "Plot generation complete!" in result.text

        # Get created PIL image from the result
        result.images[0].save(f"output.png")
```

Images are not part of the output stream, but are available as a `images` list in the `result` object. The example above saves the created image as [output.png](sine.png):

![Sine Wave](sine.png)

## Bind mounts

You can mount host directories into the container to allow code execution to access external files:

```python
# Map host paths to container paths. Host paths can be absolute or relative.
# Container paths must be relative and are created as subdirectories of the
# /app directory in the container. The /app directory is the container's
# working directory.
binds = {
    "./data": "data",  # Read data from host
    "./output": "output"  # Write results to host
}

# Create a data file on the host
async with aiofiles.open("data/input.txt", "w") as f:
    await f.write("hello world")

async with ExecutionContainer(binds=binds) as container:
    async with ExecutionClient(host="localhost", port=container.port) as client:
        # Read from mounted data directory
        result = await client.execute("""
            with open('data/input.txt') as f:
                data = f.read()

            # Process data...
            processed = data.upper()

            # Write to mounted output directory
            with open('output/result.txt', 'w') as f:
                f.write(processed)
        """)

# Check the result file on the host
async with aiofiles.open("output/result.txt", "r") as f:
    assert await f.read() == "HELLO WORLD"
```

## Environment variables

Environment variables can be passed to the container for configuration or secrets:

```python
env = {
    "API_KEY": "secret-key-123",
    "DEBUG": "1"
}

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
        print(result.text)
        # Using API key: secret-key-123
        # Debug mode enabled
```
