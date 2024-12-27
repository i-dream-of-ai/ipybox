# ipybox

`ipybox` is a lightweight, stateful and secure Python code execution sandbox built with [IPython](https://ipython.org/) and [Docker](https://www.docker.com/). Designed for AI agents that interact with their environment through code execution, it is also well-suited for general-purpose code execution. `ipybox` is fully open-source and free to use, distributed under the Apache 2.0 license.

<p align="center">
  <img src="docs/img/logo.png" alt="logo">
</p>

## Features

- **Secure Execution**: Executes code in isolated Docker containers, preventing unauthorized access to the host system
- **Stateful Execution**: Maintains variable and session state across commands using IPython kernels
- **Real-Time Output Streaming**: Provides immediate feedback through direct output streaming
- **Enhanced Plotting Support**: Enables downloading of plots created with Matplotlib and other visualization libraries
- **Flexible Dependency Management**: Supports package installation and updates during runtime or at build time
- **Resource Management**: Controls container lifecycle with built-in timeout and resource management features
- **Reproducible Environments**: Ensures consistent execution environments across different systems

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

Install pre-commit hooks:

```bash
invoke precommit-install
```

Run tests:

```bash
pytest -s tests
```
