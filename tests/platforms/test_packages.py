"""Stable asset names reject an apparently complete versioned-name inventory."""
import importlib.util
from pathlib import Path
import pytest
spec = importlib.util.spec_from_file_location('verify_packages', Path(__file__).resolve().parents[2]/'scripts/verify_packages.py')
module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
@pytest.mark.parametrize('names', [
    ['tetris-browser-0.1.0.zip', 'SHA256SUMS.txt'],
    ['tetris-browser.zip', 'tetris-browser.zip', 'SHA256SUMS.txt'],
    ['tetris-browser.zip'],
])
def test_reject_names(names):
    with pytest.raises(ValueError):
        module.verify_names(names, ['tetris-browser.zip', 'SHA256SUMS.txt'])
def test_accept_stable_names():
    module.verify_names(['tetris-browser.zip', 'SHA256SUMS.txt'], ['tetris-browser.zip', 'SHA256SUMS.txt'])
