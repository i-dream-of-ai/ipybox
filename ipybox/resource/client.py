import asyncio
from typing import Any

import aiohttp


class ConnectionError(Exception):
    """Raised when a connection to a resource server cannot be established."""


class ResourceClient:
    """Context manager for

    - loading the source code of Python modules and generated MCP client functions
      from an [`ExecutionContainer`][ipybox.container.ExecutionContainer].
    - generating Python client functions from MCP server tool metadata and storing
      the generated sources in an [`ExecutionContainer`][ipybox.container.ExecutionContainer].

    Args:
        port: Host port for the container's resource port
        host: Hostname or IP address of the container's host
        connect_retries: Number of connection retries.
        connect_retry_interval: Delay between connection retries in seconds.
    """

    def __init__(
        self,
        port: int,
        host: str = "localhost",
        connect_retries: int = 10,
        connect_retry_interval: float = 1.0,
    ):
        self.port = port
        self.host = host
        self._base_url = f"http://{self.host}:{self.port}"
        self._session: aiohttp.ClientSession = None
        self._connect_retries = connect_retries
        self._connect_retry_interval = connect_retry_interval

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        self._session = aiohttp.ClientSession()
        await self._status()

    async def disconnect(self):
        await self._session.close()

    async def _status(self) -> dict[str, str]:
        for _ in range(self._connect_retries):
            try:
                async with self._session.get(f"{self._base_url}/status") as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception:
                await asyncio.sleep(self._connect_retry_interval)
        else:
            raise ConnectionError("Failed to connect to resource server")

    async def generate_mcp_sources(self, relpath: str, server_name: str, server_params: dict[str, Any]) -> list[str]:
        """Generate Python client functions for tools provided by an MCP server.

        One MCP client function is generated per MCP tool from its metadata. The generated function is stored in a
        module named `/app/{relpath}/{server_name}/{tool_name}.py`. Importing this module and calling the function
        invokes the corresponding MCP tool. This works for both `stdio` and `sse` based MCP servers. `stdio` based
        MCP servers are executed inside the container, `sse` based MCP servers are expected to run elsewhere.

        Args:
            relpath: Path relative to the container's `/app` directory.
            server_name: An application-defined name for the MCP server. Must be a valid Python module name.
            server_params: MCP server configuration. `stdio` server configurations must specify at least a `command`
                key, `sse` server configurations must specify at least a `url` key.

        Returns:
            List of tool names provided by the MCP server. Tool names are sanitized to ensure they
                can be used as Python module names.
        """
        url = f"{self._base_url}/mcp/{relpath}/{server_name}"
        async with self._session.put(url, json=server_params) as response:
            response.raise_for_status()
            return await response.json()

    async def get_mcp_sources(self, relpath: str, server_name: str) -> dict[str, str]:
        """Get the source code of generated MCP client functions for given MCP `server_name`.

        Args:
            relpath: Path relative to the container's `/app` directory
            server_name: Application-defined name of an MCP server

        Returns:
            Source code of generated MCP client functions. Keys are tool names, values are generated sources.
        """
        url = f"{self._base_url}/mcp/{relpath}"
        async with self._session.get(url, params={"server_name": server_name}) as response:
            response.raise_for_status()
            return await response.json()

    async def get_module_sources(self, module_names: list[str]) -> dict[str, str]:
        """Get the source code of Python modules on the container's Python path.

        Args:
            module_names: A list of Python module names.

        Returns:
            Source code of Python modules. Keys are module names, values are module sources.
        """
        url = f"{self._base_url}/modules"
        async with self._session.get(url, params={"q": module_names}) as response:
            response.raise_for_status()
            return await response.json()
