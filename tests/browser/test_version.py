"""Built renderer version must match the source/package release metadata."""
import json
from pathlib import Path
from playwright.sync_api import expect

def test_renderer_version_matches_project(page):
    version=json.loads((Path(__file__).resolve().parents[2]/'package.json').read_text())['version']
    expect(page.locator('.edition')).to_contain_text(version)
