import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import aiofiles
import pytest
from PIL import Image

from gradion.executor import ExecutionClient, ExecutionContainer, ExecutionError


@pytest.fixture(scope="module")
async def workspace():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="module")
def executor_image() -> Generator[str, None, None]:
    tag = "executor-test"
    deps_path = Path(__file__).parent / "dependencies.txt"

    # Build the image using the CLI
    subprocess.run(
        ["python", "-m", "gradion.executor", "build", "-t", tag, "-d", str(deps_path)],
        check=True,
    )

    yield tag


@pytest.fixture(scope="module")
async def executor(executor_image: str, workspace: Path):
    async with ExecutionContainer(
        tag=executor_image,
        binds={workspace: "workspace"},
        env={"TEST_VAR": "test_val"},
    ) as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            yield client


@pytest.mark.asyncio(loop_scope="module")
async def test_single_command_output(executor):
    result = await executor.execute("print('Hello, world!')")
    assert result.text == "Hello, world!"


@pytest.mark.asyncio(loop_scope="module")
async def test_multi_command_output(executor):
    code = """
print('first')
print('second')
print('third')
"""
    result = await executor.execute(code)
    assert result.text == "first\nsecond\nthird"


@pytest.mark.asyncio(loop_scope="module")
async def test_no_output(executor):
    result = await executor.execute("x = 1")
    assert result.text is None


@pytest.mark.asyncio(loop_scope="module")
async def test_long_output(executor):
    result = await executor.execute("print('a' * 500000)")
    assert result.text == "a" * 500000


@pytest.mark.asyncio(loop_scope="module")
async def test_long_output_multiline(executor):
    result = await executor.execute("""s = "a\\n" * 500000; print(s)""")
    assert result.text == ("a\n" * 500000).strip()


@pytest.mark.asyncio(loop_scope="module")
async def test_long_output_chunked(executor):
    code = """
import asyncio

for i in range(100):
    print("a")
    await asyncio.sleep(0.01)
"""
    result = await executor.execute(code)
    assert result.text == ("a\n" * 100).strip()


@pytest.mark.asyncio(loop_scope="module")
async def test_image_output(executor):
    code = """
from PIL import Image
import numpy as np

# Create a simple test image
img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
img.show()
"""
    result = await executor.execute(code)
    assert len(result.images) == 1
    assert isinstance(result.images[0], Image.Image)
    assert result.images[0].size == (100, 100)


@pytest.mark.asyncio(loop_scope="module")
async def test_multiple_image_output(executor):
    code = """
from PIL import Image
import numpy as np

# Create two test images
img1 = Image.fromarray(np.zeros((50, 50, 3), dtype=np.uint8))
img2 = Image.fromarray(np.ones((30, 30, 3), dtype=np.uint8) * 255)
img1.show()
img2.show()
"""
    result = await executor.execute(code)
    assert len(result.images) == 2
    assert isinstance(result.images[0], Image.Image)
    assert isinstance(result.images[1], Image.Image)
    assert result.images[0].size == (50, 50)
    assert result.images[1].size == (30, 30)


@pytest.mark.asyncio(loop_scope="module")
async def test_long_input(executor):
    code = "result = 0\n"
    code += "\n".join(f"result += {i}" for i in range(10000))
    code += "\nprint(result)"
    result = await executor.execute(code)
    assert result.text == str(sum(range(10000)))


@pytest.mark.asyncio(loop_scope="module")
async def test_runtime_error(executor):
    with pytest.raises(ExecutionError) as exc_info:
        await executor.execute("2 / 0")
    assert "ZeroDivisionError" in exc_info.value.args[0]
    assert "ZeroDivisionError" in exc_info.value.trace


@pytest.mark.asyncio(loop_scope="module")
async def test_syntax_error(executor):
    code = "while True print('Hello')"
    with pytest.raises(ExecutionError) as exc_info:
        await executor.execute(code)
    assert "SyntaxError" in exc_info.value.args[0]
    assert "SyntaxError" in exc_info.value.trace


@pytest.mark.asyncio(loop_scope="module")
async def test_interrupt_kernel(executor):
    code = """
a = 0
while True:
    a = 5
"""
    with pytest.raises(asyncio.TimeoutError):
        await executor.execute(code, timeout=1)
    result = await executor.execute("print(a)")
    assert result.text == "5"


@pytest.mark.asyncio(loop_scope="module")
async def test_env(executor: ExecutionClient):
    result = await executor.execute("import os; print(os.environ['TEST_VAR'])")
    assert result.text == "test_val"


@pytest.mark.asyncio(loop_scope="module")
async def test_binds(executor: ExecutionClient, workspace: Path):
    async with aiofiles.open(workspace / "test_file", "w") as f:
        await f.write("test_content")

    result = await executor.execute("import os; print(open('workspace/test_file').read())")
    assert result.text == "test_content"
