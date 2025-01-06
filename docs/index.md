# Overview

`ipybox` is a lightweight, stateful and secure Python code execution sandbox built with [IPython](https://ipython.org/) and [Docker](https://www.docker.com/). Designed for AI agents that interact with their environment through code execution, like the [`freeact`](https://gradion-ai.github.io/freeact/) agent system, it is also well-suited for general-purpose code execution. `ipybox` is fully open-source and free to use, distributed under the Apache 2.0 license.

<figure markdown>
  ![logo](img/logo.png){ width="400" style="display: block; margin: 0 auto" }
</figure>

## Features

- **Secure Execution**: Executes code in isolated Docker containers, preventing unauthorized access to the host system
- **Stateful Execution**: Maintains variable and session state across commands using IPython kernels
- **Real-Time Output Streaming**: Provides immediate feedback through direct output streaming
- **Enhanced Plotting Support**: Enables downloading of plots created with Matplotlib and other visualization libraries
- **Flexible Dependency Management**: Supports package installation and updates during runtime or at build time
- **Resource Management**: Controls container lifecycle with built-in timeout and resource management features
- **Reproducible Environments**: Ensures consistent execution environments across different systems
