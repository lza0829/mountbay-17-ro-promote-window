# -*- coding: utf-8 -*-
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
smoke = ROOT / "data-live2"
shutil.rmtree(smoke, ignore_errors=True)
os.environ["数据目录"] = str(smoke)
py = ROOT / ".venv" / "Scripts" / "uvicorn.exe"
p = subprocess.Popen(
    [str(py), "app.main:app", "--host", "127.0.0.1", "--port", "12201"],
    cwd=str(ROOT),
    env={**os.environ},
)
time.sleep(2)
B = "http://127.0.0.1:12201"


def call(method, path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        B + path,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if body else {},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


try:
    print("health", call("GET", "/" + quote("健康")))
    st, ns = call("POST", "/" + quote("演示") + "/" + quote("入册"), {})
    print("ns", st, ns)
    st, m = call(
        "POST",
        "/" + quote("演示") + "/" + quote("申请挂载"),
        {"名空间键": ns["名空间键"], "源路径": "/a", "目标路径": "/b"},
    )
    print("m", st, m)
    st, b = call("POST", "/" + quote("演示") + "/" + quote("占忙点"), {"挂载号": m["挂载号"]})
    print("b", st, b)
    path = "/" + quote("挂载卸载") + "/" + m["挂载号"]
    print("path", path, call("POST", path))
    path2 = "/" + quote("忙点释放") + "/" + b["忙点号"]
    print("release", call("POST", path2))
    print("umount2", call("POST", path))
    print("verify", call("GET", "/" + quote("载界验")))
finally:
    p.terminate()
    p.wait(timeout=5)
