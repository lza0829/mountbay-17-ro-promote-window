# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
smoke = ROOT / "data-smoke"
if smoke.exists():
    shutil.rmtree(smoke)
os.environ["数据目录"] = str(smoke)
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as c:
    assert c.get("/健康").json()["ok"] is True
    ns = c.post("/演示/入册", json={"别名": "烟测"}).json()
    assert "名空间键" in ns
    m = c.post(
        "/演示/申请挂载",
        json={"名空间键": ns["名空间键"], "源路径": "/a", "目标路径": "/b"},
    ).json()
    assert m["状态"] == "已挂"
    b = c.post("/演示/占忙点", json={"挂载号": m["挂载号"]}).json()
    r = c.post(f"/mnt/{m['挂载号']}/umount")
    assert r.status_code == 409, r.text
    assert c.post(f"/busy/{b['忙点号']}/release").json()["状态"] == "已释放"
    assert c.post(f"/mnt/{m['挂载号']}/umount").json()["状态"] == "已卸"
    v = c.get("/载界验").json()
    assert v["valid"] is True, v
    print("SMOKE OK", v)
