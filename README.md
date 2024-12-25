# ipybox

`ipybox` is a lightweight, stateful and secure Python code execution sandbox built with [IPython](https://ipython.org/) and [Docker](https://www.docker.com/). Designed for AI agents that interact with their environment through code execution, it is also well-suited for general-purpose code execution. Fully open-source and free to use, ipybox is distributed under the Apache 2.0 license.

<p align="center">
  <img src="docs/img/logo.png" alt="logo">
</p>

## Features

- **Secure Execution**: Executes code in isolated Docker containers, preventing unauthorized access to the host system.
- **Stateful Execution**: Retains variable and session state across commands using IPython kernels.
- **Real-Time Output Streaming**: Streams execution outputs directly, enabling real-time feedback.
- **Enhanced Plotting Support**: Facilitates downloading plots created with Matplotlib and other libraries.
- **Flexible Dependency Management**: Supports installing and updating dependencies during runtime or at build time.
- **Resource Management**: Manages container lifecycle with built-in timeout and resource control mechanisms.
- **Reproducible Environments**: Provides a consistent execution setup across different systems to ensure reproducibility.

## Status

Ipybox is in an early stage of development, with ongoing refinements and enhancements to its core features. Community feedback and contributions are greatly appreciated as ipybox continues to evolve.

## Documentation

The official documentation is available [here](https://gradion-ai.github.io/ipybox/).

## Quickstart

Install `ipybox` Python package:

```bash
pip install ipybox
```

Build a `gradion-ai/ipybox` Docker image:

```bash
python -m ipybox build -t gradion-ai/ipybox
```

Print something inside `ipybox`:

```python
import asyncio
from ipybox import ExecutionClient, ExecutionContainer

async def main():
    async with ExecutionContainer(tag="gradion-ai/ipybox") as container:
        async with ExecutionClient(port=container.port) as client:
            result = await client.execute("print('Hello, world!')")
            print(f"Output: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

Find out more in the [user guide](https://gradion-ai.github.io/ipybox/).

## Development

Clone the repository:

```bash
git clone https://github.com/gradion-ai/ipybox.git
cd ipybox
```

Create a new Conda environment and activate it:

```bash
conda env create -f environment.yml
conda activate ipybox
```

Install dependencies with Poetry:

```bash
poetry install --with docs
```

Run tests:

```bash
pytest -s tests
```
