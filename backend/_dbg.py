# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

smoke = Path(__file__).resolve().parent / "data-smoke2"
shutil.rmtree(smoke, ignore_errors=True)
os.environ["数据目录"] = str(smoke)

from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as c:
    print([getattr(r, "path", None) for r in app.routes])
    ns = c.post("/演示/入册", json={"别名": "x"}).json()
    print("ns", ns)
    m = c.post(
        "/演示/申请挂载",
        json={"名空间键": ns["名空间键"], "源路径": "/a", "目标路径": "/b"},
    ).json()
    print("m", m)
    b = c.post("/演示/占忙点", json={"挂载号": m["挂载号"]}).json()
    print("b", b)
    url = f"/挂载账/{m['挂载号']}/卸载"
    print("url", url)
    r = c.post(url)
    print(r.status_code, r.text)
