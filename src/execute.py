# nodeServer_exec  –  auto-launch Node server AND open browser on start
import subprocess, os, signal, threading, time, webbrowser

import platform

# ─── configuration ───────────────────────────────────────────────
# Set NODE_CMD depending on OS
if platform.system() == 'Windows':
    NODE_CMD = 'node'  # assume in PATH
elif platform.system() == 'Darwin':
    NODE_CMD = '/opt/homebrew/bin/node'  # replace with actual path to node on macOS
else:
    NODE_CMD = 'node'  # default fallback (may need adjustment)

SERVER_JS  = os.path.join(project.folder, 'src', 'server.js')
SERVER_PORT = 9980                             # must match server.js
AUTO_OPEN_BROWSER = True                       # set False to disable
# ─────────────────────────────────────────────────────────────────

proc = None   # will hold subprocess.Popen

def _launch_browser():
    """Wait a moment, then open the web UI once per TD launch."""
    time.sleep(1)  # wait for server to start listening
    url = f'http://localhost:{SERVER_PORT}'
    webbrowser.open(url)
    print('Web server browser opened →', url)

def onStart():
    global proc
    if proc is None:
        proc = subprocess.Popen(
            [NODE_CMD, SERVER_JS],
            cwd=os.path.dirname(SERVER_JS),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print('Web server started')
        if AUTO_OPEN_BROWSER:
            threading.Thread(target=_launch_browser, daemon=True).start()
    return

def onExit():
    global proc
    if proc and proc.poll() is None:           # still running?
        try:
            proc.send_signal(signal.SIGINT)    # graceful shutdown
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
        print('Web server stopped')
    proc = None
    return
