import subprocess
import sys

from giwaxs_toolbox import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "giwaxs_toolbox", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
