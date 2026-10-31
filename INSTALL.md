# Installation and controls

## Browser

Extract tetris-browser.zip into one directory. Serve that directory through ordinary static HTTP(S) hosting, then open its index page. No application backend or Node.js runtime is needed to play. For a local test with Python available, run python -m http.server 8000 from the extracted directory and open http://localhost:8000. Opening the page as a file URL is unsupported for persistence.

## Keyboard

Start with the left Start button. Left/Right move, Down soft drops, Up or Space rotates clockwise, Z rotates back, Enter hard drops, C holds, P pauses/resumes and R restarts. A grounded piece locks after one full gravity interval; hard drop follows that delay and movement on the ground does not restart it. The two information-panel gameplay buttons are Start/Restart and Pause/Start. Losing focus pauses; return and resume explicitly.

## Distribution status

The browser bundle is a static deployment artifact. Windows and sidebar packages are not included in the browser releases. Later platforms are unsigned development distributions unless a release explicitly says otherwise; no store distribution or signing is implied.
