"""
Datahost — Hosting Login Checker

Entry point. Jalankan dengan:
    python datahost.py
"""

import os
import subprocess
import sys


def _spawn_watchdog() -> None:
    """Spawn proses watchdog TERPISAH yang tetap hidup walau proses utama
    stuck/crash -- heartbeat + commands-poll jalan independen. Watchdog
    menerima PID proses ini supaya bisa monitor apakah masih hidup."""
    watchdog_script = os.path.join(os.path.dirname(__file__), "app", "watchdog.py")
    if not os.path.exists(watchdog_script):
        return
    my_pid = os.getpid()
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        )
    subprocess.Popen(
        [sys.executable, watchdog_script, str(my_pid)],
        cwd=os.path.dirname(__file__),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        **kwargs,
    )


if __name__ == "__main__":
    _spawn_watchdog()
    from app.runner import run
    run()
