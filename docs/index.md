# Overview

`ipybox` is a lightweight, stateful and secure Python code execution sandbox built with [IPython](https://ipython.org/) and [Docker](https://www.docker.com/). Designed for AI agents that interact with their environment through code execution, it is also well-suited for general-purpose code execution. Fully open-source and free to use, ipybox is distributed under the Apache 2.0 license.

<figure markdown>
  ![logo](img/logo.png){ width="400" style="display: block; margin: 0 auto" }
</figure>

## Features

- **Secure Execution**: Executes code in isolated Docker containers, preventing unauthorized access to the host system.
- **Stateful Execution**: Retains variable and session state across commands using IPython kernels.
- **Real-Time Output Streaming**: Streams execution outputs directly, enabling real-time feedback.
- **Enhanced Plotting Support**: Facilitates downloading plots created with Matplotlib and other libraries.
- **Flexible Dependency Management**: Supports installing and updating dependencies during runtime or at build time.
- **Resource Management**: Manages container lifecycle with built-in timeout and resource control mechanisms.
- **Reproducible Environments**: Provides a consistent execution setup across different systems to ensure reproducibility.

## Status

`ipybox` is in an early stage of development, with ongoing refinements and enhancements to its core features. Community feedback and contributions are greatly appreciated as `ipybox` continues to evolve.
