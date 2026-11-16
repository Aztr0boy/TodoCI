"""Stage a TodoCI deployment, smoke-test it, and create the Jenkins artifact."""
import json
import os
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
APP_FILES = ("todo.py", "storage.py", "app.py", "server.py")
ARTIFACT = ROOT / "todo-app.tar.gz"


def _request(url, data=None):
    headers = {"Content-Type": "application/json"} if data is not None else {}
    request = Request(url, data=data, headers=headers)
    with urlopen(request, timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _stop_server(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    if process.stdout:
        output = process.stdout.read()
        if output:
            print(output, end="")


def main():
    with tempfile.TemporaryDirectory(prefix="todoci-deploy-") as temp:
        deploy_dir = Path(temp) / "deploy"
        static_dir = deploy_dir / "static"
        static_dir.mkdir(parents=True)
        for name in APP_FILES:
            shutil.copy2(ROOT / name, deploy_dir / name)
        shutil.copy2(ROOT / "static" / "index.html", static_dir / "index.html")

        port = _free_port()
        data_file = Path(temp) / "smoke.json"
        process = subprocess.Popen(
            [
                sys.executable,
                str(deploy_dir / "server.py"),
                "--port",
                str(port),
                "--host",
                "127.0.0.1",
                "--file",
                str(data_file),
            ],
            cwd=deploy_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, "TODOCI_QUIET": "1"},
        )
        base_url = "http://127.0.0.1:%d" % port

        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    output, _ = process.communicate()
                    raise RuntimeError("Deployed server exited early:\n" + output)
                try:
                    health = _request(base_url + "/health")
                    if health.get("status") == "ok":
                        break
                except (OSError, URLError, TimeoutError):
                    time.sleep(0.25)
            else:
                raise RuntimeError("Deployed server did not become healthy within 10 seconds")

            print("Health check:", health)
            created = _request(
                base_url + "/api/tasks",
                json.dumps(
                    {"title": "Jenkins smoke test", "priority": "high"}
                ).encode("utf-8"),
            )
            if created.get("title") != "Jenkins smoke test":
                raise RuntimeError("Smoke-test task was not created correctly")
            print("Create task:", created)

            stats = _request(base_url + "/api/stats")
            if stats.get("total") != 1 or stats["open_by_priority"].get("high") != 1:
                raise RuntimeError("Smoke-test stats did not match the created task")
            print("Stats check:", stats)
        finally:
            _stop_server(process)

        with tarfile.open(ARTIFACT, "w:gz") as archive:
            for path in deploy_dir.rglob("*"):
                if path.is_file():
                    archive.add(path, arcname=path.relative_to(deploy_dir).as_posix())
        print("Created artifact:", ARTIFACT)


if __name__ == "__main__":
    main()
