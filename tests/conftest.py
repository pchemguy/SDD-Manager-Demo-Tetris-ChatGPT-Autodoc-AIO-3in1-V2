"""Project-local deterministic drivers shared by pytest scenarios."""
import json
import subprocess
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
@pytest.fixture
def driver():
    def run(op, **values):
        result = subprocess.run(['node', '.test-build/tests/support/driver.js'], cwd=ROOT, input=json.dumps({'op': op, **values}), text=True, capture_output=True, timeout=15)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    return run
