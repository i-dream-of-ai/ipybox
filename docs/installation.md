# Installation

Installation is simple with:

```bash
pip install ipybox
```

## Container image

!!! note

    Building the container image requires [Docker](https://www.docker.com/) to be installed. Containers will run with the same user and group IDs as the user who built the image, ensuring proper file permissions on mounted host directories.

### Default build

To build a container image with default settings and no extra dependencies:

```bash
python -m ipybox build
```

This creates a Docker image tagged as `gradion/ipybox` with base Python dependencies required for the code execution environment.

### Custom build

To create a custom image with additional dependencies for your application, create a dependencies file (e.g., `dependencies.txt`) following. For example:

```txt
pandas = "^2.2"
scikit-learn = "^1.5"
matplotlib = "^3.9"
```

To build the image with custom tag and dependencies:

```bash
python -m ipybox build \
    --tag my-box:v1 \
    --dependencies path/to/dependencies.txt
```

The dependencies file should list Python packages in [Poetry dependency specification format](https://python-poetry.org/docs/dependency-specification/). These will be installed in addition to the base dependencies required for the execution environment. The execution container also supports [installing dependencies at runtime](usage.md#installing-dependencies-at-runtime).
