"""Isolated managed-browser contexts serving the actual production build."""
import functools
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
@pytest.fixture(scope='session')
def app_url():
    handler = functools.partial(QuietHandler, directory=os.environ.get('TETRIS_WEB_ROOT',str(ROOT/'dist/browser')))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True);thread.start()
    yield f'http://127.0.0.1:{server.server_port}'
    server.shutdown();server.server_close();thread.join(timeout=5)
@pytest.fixture
def page(app_url):
    with sync_playwright() as p:
        engine = os.environ.get('TETRIS_BROWSER', 'chromium')
        options = {'headless': True, 'timeout': 10000}
        if engine == 'firefox':
            options['env'] = {**os.environ, 'MOZ_DISABLE_CONTENT_SANDBOX': '1'}
        browser = getattr(p, engine).launch(**options)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = context.new_page();page.set_default_timeout(5000)
        errors = [];page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(app_url)
        yield page
        assert errors == [], errors
        context.close();browser.close()
