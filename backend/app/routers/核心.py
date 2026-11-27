from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.db import 连接

api = APIRouter()


def 此刻() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def 行(r) -> dict:
    return dict(r) if r is not None else {}


class 名空间入(BaseModel):
    别名: str = "演示名空间"
    类型: str = "主机"
    说明: str = ""


class 挂载入(BaseModel):
    名空间键: str
    源路径: str = "/demo/src"
    目标路径: str = "/mnt/demo"
    模式: str = "bind"
    传播: str = "private"
    只读: bool = False


class 传播入(BaseModel):
    传播: str = Field(description="private|shared|slave")


class 忙点入(BaseModel):
    挂载号: str
    占用说明: str = "演示占用"


@api.get("/健康")
def 健康():
    return {"ok": True, "名": "载界"}


@api.get("/总览")
def 总览():
    with 连接() as c:
        ns = c.execute("SELECT COUNT(*) n FROM 名空间册").fetchone()["n"]
        m = c.execute("SELECT COUNT(*) n FROM 挂载账 WHERE 状态='已挂'").fetchone()["n"]
        b = c.execute("SELECT COUNT(*) n FROM 忙点闸 WHERE 状态='占用'").fetchone()["n"]
    return {"名空间数": ns, "已挂数": m, "忙点数": b}


@api.get("/名空间册")
def 名空间列表():
    with 连接() as c:
        rows = c.execute("SELECT * FROM 名空间册 ORDER BY 入册时 DESC").fetchall()
    return [行(r) for r in rows]


@api.post("/演示/入册")
def 演示入册(body: 名空间入 | None = None):
    body = body or 名空间入()
    key = "ns-" + uuid.uuid4().hex[:8]
    with 连接() as c:
        c.execute(
            "INSERT INTO 名空间册(名空间键,别名,类型,说明,入册时) VALUES (?,?,?,?,?)",
            (key, body.别名, body.类型, body.说明, 此刻()),
        )
        c.commit()
        r = c.execute("SELECT * FROM 名空间册 WHERE 名空间键=?", (key,)).fetchone()
    return 行(r)


@api.get("/挂载账")
def 挂载列表():
    with 连接() as c:
        rows = c.execute("SELECT * FROM 挂载账 ORDER BY 申请时 DESC").fetchall()
    return [行(r) for r in rows]


@api.post("/演示/申请挂载")
def 申请挂载(body: 挂载入):
    with 连接() as c:
        ns = c.execute("SELECT 1 FROM 名空间册 WHERE 名空间键=?", (body.名空间键,)).fetchone()
        if not ns:
            raise HTTPException(400, "名空间不存在")
        mid = "mnt-" + uuid.uuid4().hex[:8]
        c.execute(
            """INSERT INTO 挂载账(挂载号,名空间键,源路径,目标路径,模式,传播,状态,只读,申请时)
               VALUES (?,?,?,?,?,?, '已挂', ?, ?)""",
            (
                mid,
                body.名空间键,
                body.源路径,
                body.目标路径,
                body.模式,
                body.传播,
                1 if body.只读 else 0,
                此刻(),
            ),
        )
        c.commit()
        r = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (mid,)).fetchone()
    return 行(r)


@api.post("/mnt/{mount_id}/prop")
def 设传播(mount_id: str, body: 传播入):
    if body.传播 not in ("private", "shared", "slave"):
        raise HTTPException(400, "传播须为 private|shared|slave")
    with 连接() as c:
        r = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (mount_id,)).fetchone()
        if not r:
            raise HTTPException(404, "挂载不存在")
        if r["状态"] != "已挂":
            raise HTTPException(400, "仅已挂可改传播")
        c.execute("UPDATE 挂载账 SET 传播=? WHERE 挂载号=?", (body.传播, mount_id))
        c.commit()
        r = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (mount_id,)).fetchone()
    return 行(r)


@api.get("/忙点闸")
def 忙点列表():
    with 连接() as c:
        rows = c.execute("SELECT * FROM 忙点闸 ORDER BY 占用时 DESC").fetchall()
    return [行(r) for r in rows]


@api.post("/演示/占忙点")
def 占忙点(body: 忙点入):
    with 连接() as c:
        m = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (body.挂载号,)).fetchone()
        if not m:
            raise HTTPException(404, "挂载不存在")
        if m["状态"] != "已挂":
            raise HTTPException(400, "仅已挂可占忙点")
        bid = "busy-" + uuid.uuid4().hex[:8]
        c.execute(
            "INSERT INTO 忙点闸(忙点号,挂载号,占用说明,状态,占用时) VALUES (?,?,?,'占用',?)",
            (bid, body.挂载号, body.占用说明, 此刻()),
        )
        c.commit()
        r = c.execute("SELECT * FROM 忙点闸 WHERE 忙点号=?", (bid,)).fetchone()
    return 行(r)


@api.post("/busy/{busy_id}/release")
def 释放忙点(busy_id: str):
    with 连接() as c:
        b = c.execute("SELECT * FROM 忙点闸 WHERE 忙点号=?", (busy_id,)).fetchone()
        if not b:
            raise HTTPException(404, "忙点不存在")
        if b["状态"] != "占用":
            raise HTTPException(400, "已释放")
        c.execute(
            "UPDATE 忙点闸 SET 状态='已释放', 释放时=? WHERE 忙点号=?",
            (此刻(), busy_id),
        )
        c.commit()
        r = c.execute("SELECT * FROM 忙点闸 WHERE 忙点号=?", (busy_id,)).fetchone()
    return 行(r)


@api.post("/mnt/{mount_id}/umount")
def 卸载(mount_id: str):
    with 连接() as c:
        m = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (mount_id,)).fetchone()
        if not m:
            raise HTTPException(404, "挂载不存在")
        if m["状态"] != "已挂":
            raise HTTPException(400, "已非已挂")
        busy = c.execute(
            "SELECT COUNT(*) n FROM 忙点闸 WHERE 挂载号=? AND 状态='占用'",
            (mount_id,),
        ).fetchone()["n"]
        if busy:
            raise HTTPException(409, f"忙点占用中({busy})，拒绝卸载")
        c.execute(
            "UPDATE 挂载账 SET 状态='已卸', 卸载时=? WHERE 挂载号=?",
            (此刻(), mount_id),
        )
        c.commit()
        r = c.execute("SELECT * FROM 挂载账 WHERE 挂载号=?", (mount_id,)).fetchone()
    return 行(r)


@api.get("/载界验")
def 载界验():
    with 连接() as c:
        mounts = [行(r) for r in c.execute("SELECT * FROM 挂载账").fetchall()]
        busy = [行(r) for r in c.execute("SELECT * FROM 忙点闸 WHERE 状态='占用'").fetchall()]
        ns = [行(r) for r in c.execute("SELECT * FROM 名空间册").fetchall()]
    active = [m for m in mounts if m["状态"] == "已挂"]
    issues = []
    for m in active:
        if m["传播"] not in ("private", "shared", "slave"):
            issues.append(f"{m['挂载号']} 传播非法")
    busy_ids = {b["挂载号"] for b in busy}
    for m in mounts:
        if m["状态"] == "已挂" and m["挂载号"] in busy_ids:
            # 有忙点是合法态，仅记录
            pass
    ok = len(ns) >= 1 and len(active) + sum(1 for m in mounts if m["状态"] == "已卸") >= 1 and not issues
    return {
        "valid": ok,
        "名空间数": len(ns),
        "已挂数": len(active),
        "忙点数": len(busy),
        "说明": "名空间、挂载与忙点账可对上；忙点占用时卸载应被拒绝。" if ok else "缺演示链路或传播非法",
        "issues": issues,
    }
