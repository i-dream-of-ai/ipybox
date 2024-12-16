# ipybox

A secure, lightweight Python code execution sandbox based on IPython and Docker, specifically designed for AI/ML applications and LLM agents.

![logo](logo.png)

## Overview

This project provides a sandboxed Python code execution environment built on IPython and Docker. It offers:

- **Secure Execution**: Code runs in Docker containers, preventing unauthorized system access
- **Flexible Dependencies**: Supports static and runtime dependency management
- **Real-time Streaming**: Chunked streaming of execution output as it's generated
- **Image Support**: Handle image outputs from matplotlib and other visualization libraries
- **Resource Control**: Container lifecycle management and built-in timeout mechanisms
- **Reproducible Environment**: Consistent execution environment across different systems
- **LLM Agent Ready**: Ideal for AI applications that need to execute Python code

This project is in early beta, with active development of new features ongoing.
