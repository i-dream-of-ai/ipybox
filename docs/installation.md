# Installation

```bash
pip install ipybox
```

## Docker image

Before using `ipybox`, you need to build a Docker image. This image contains all required dependencies for executing Python code in stateful and isolated sessions.

!!! note

    Building an `ipybox` Docker image requires [Docker](https://www.docker.com/) to be installed on your system. Containers created from this image will run with the same user and group IDs as the user who built the image, ensuring proper file permissions on mounted host directories.

### Default build

To build an `ipybox` Docker image with default settings:

```bash
python -m ipybox build
```

This creates a Docker image tagged as `gradion-ai/ipybox` containing the base Python dependencies required for the code execution environment.

### Custom build

To create a custom `ipybox` Docker image with additional dependencies, create a dependencies file (e.g., `dependencies.txt`). For example:

```toml title="dependencies.txt"
pandas = "^2.2"
scikit-learn = "^1.5"
matplotlib = "^3.9"
```

Then build the image with a custom tag and dependencies:

```bash
python -m ipybox build -t my-box:v1 -d path/to/dependencies.txt
```

The dependencies file should use the [Poetry dependency specification format](https://python-poetry.org/docs/dependency-specification/). These packages will be installed alongside the base dependencies required for the execution environment. You can also [install additional dependencies at runtime](usage.md#installing-dependencies-at-runtime).
