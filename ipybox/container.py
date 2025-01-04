from collections import defaultdict
from pathlib import Path

from aiodocker import Docker

from ipybox.utils import arun

DEFAULT_TAG = "gradion-ai/ipybox"


class ExecutionContainer:
    """
    A context manager for managing the lifecycle of a Docker container used for code execution.

    It handles the creation, port mapping, volume binding, and cleanup of the container.

    Args:
        tag: Tag of the Docker image to use (defaults to gradion-ai/ipybox)
        binds: Mapping of host paths to container paths for volume mounting.
            Host paths may be relative or absolute. Container paths must be relative
            and are created as subdirectories of `/app` in the container.
        env: Environment variables to set in the container
        port: Host port to map to the container's executor port. If not provided,
            a random port will be allocated.
        show_pull_progress: Whether to show progress when pulling the Docker image.

    Attributes:
        port: Host port mapped to the container's executor port. This port is dynamically
            allocated when the container is started.

    Example:
        ```python
        from ipybox import ExecutionClient, ExecutionContainer

        binds = {"/host/path": "example/path"}
        env = {"API_KEY": "secret"}

        async with ExecutionContainer(binds=binds, env=env) as container:
            async with ExecutionClient(host="localhost", port=container.port) as client:
                result = await client.execute("print('Hello, world!')")
                print(result.text)
        ```
        > Hello, world!
    """

    def __init__(
        self,
        tag: str = DEFAULT_TAG,
        binds: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        port: int | None = None,
        show_pull_progress: bool = True,
    ):
        self.tag = tag
        self.binds = binds or {}
        self.env = env or {}
        self.show_pull_progress = show_pull_progress

        self._docker = None
        self._container = None
        self._port = port

    async def __aenter__(self):
        await self.run()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()

    @property
    def port(self) -> int:
        """
        The host port mapped to the container's executor port.

        This port is dynamically allocated when the container is started unless
        explicitly provided.

        Raises:
            RuntimeError: If the container is not running
        """
        if self._port is None:
            raise RuntimeError("Container not running")
        return self._port

    async def kill(self):
        """
        Kill and remove the Docker container.
        """
        if self._container:
            await self._container.kill()

        if self._docker:
            await self._docker.close()

    async def run(self):
        """
        Create and start the Docker container.
        """
        self._docker = Docker()
        self._container = await self._run()

    async def _run(self, executor_port: int = 8888):
        host_port = {"HostPort": str(self._port)} if self._port else {}

        config = {
            "Image": self.tag,
            "HostConfig": {
                "PortBindings": {
                    f"{executor_port}/tcp": [host_port]  # random host port
                },
                "AutoRemove": True,
                "Binds": await self._container_binds(),
            },
            "Env": self._container_env(),
            "ExposedPorts": {f"{executor_port}/tcp": {}},
        }

        if not await self._local_image():
            await self._pull_image()

        container = await self._docker.containers.create(config=config)  # type: ignore
        await container.start()

        container_info = await container.show()
        self._port = int(container_info["NetworkSettings"]["Ports"][f"{executor_port}/tcp"][0]["HostPort"])

        return container

    async def _local_image(self) -> bool:
        tag = self.tag if ":" in self.tag else f"{self.tag}:latest"

        images = await self._docker.images.list()  # type: ignore
        for img in images:
            if "RepoTags" in img and tag in img["RepoTags"]:
                return True

        return False

    async def _pull_image(self):
        # Track progress by layer ID
        layer_progress = defaultdict(str)

        async for message in self._docker.images.pull(self.tag, stream=True):  # type: ignore
            if not self.show_pull_progress:
                continue

            if "status" in message:
                status = message["status"]
                if "id" in message:
                    layer_id = message["id"]
                    if "progress" in message:
                        layer_progress[layer_id] = f"{status}: {message['progress']}"
                    else:
                        layer_progress[layer_id] = status

                    # Clear screen and move cursor to top
                    print("\033[2J\033[H", end="")
                    # Print all layer progress
                    for layer_id, progress in layer_progress.items():
                        print(f"{layer_id}: {progress}")
                else:
                    # Status without layer ID (like "Downloading" or "Complete")
                    print(f"\r{status}", end="")

        if self.show_pull_progress:
            print()

    async def _container_binds(self) -> list[str]:
        container_binds = []
        for host_path, container_path in self.binds.items():
            host_path_resolved = await arun(self._prepare_host_path, host_path)
            container_binds.append(f"{host_path_resolved}:/app/{container_path}")
        return container_binds

    def _prepare_host_path(self, host_path: str) -> Path:
        resolved = Path(host_path).resolve()
        if not resolved.exists():
            resolved.mkdir(parents=True)
        return resolved

    def _container_env(self) -> list[str]:
        return [f"{k}={v}" for k, v in self.env.items()]
