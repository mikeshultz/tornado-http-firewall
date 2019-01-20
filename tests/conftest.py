import os
import pytest
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

RECURSUION_MAX = 10
TMP_DIR = Path('/tmp').joinpath('http_firewall-{}'.format(
    int(datetime.now().timestamp())
))


def delete_path_recursively(pth, depth=0):
    """ Delete a path and everything under it """
    assert isinstance(pth, Path)
    assert str(pth).startswith('/tmp')  # Only temp files.
    if depth > RECURSUION_MAX:
        raise Exception('Max recursion depth!')
    if not pth.exists():
        return False
    if pth.is_file() or pth.is_symlink():
        pth.unlink()
    elif pth.is_dir():
        for child in pth.iterdir():
            delete_path_recursively(child, depth+1)
        pth.rmdir()
    else:
        raise Exception("Unable to remove {}".format(str(pth)))


@pytest.fixture
def temp_dir():
    @contextmanager
    def yield_temp_dir(tmpdir=TMP_DIR):
        temp_dir = tmpdir.joinpath('temp-{}'.format(
            datetime.now().timestamp()
        ))
        temp_dir.mkdir(parents=True)
        original_pwd = Path.cwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(original_pwd)
        delete_path_recursively(temp_dir)
    return yield_temp_dir
