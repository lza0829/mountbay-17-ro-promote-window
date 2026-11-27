from app.db import 连接

STUBS = [
    "绑定递归",
    "传播切换撕裂",
    "忙点半截卸载",
    "跨名空间窥视",
    "只读叠写",
    "卸载序闸",
    "循环挂载检出",
    "延迟卸载",
    "挂载命名冲突",
    "根转移可见性",
    "叠挂覆盖裁决",
    "传播涟漪拒卸",
    "名空间冻结写闸",
    "挂载快照钉",
    "忙点继承",
    "卸载回声账",
    "只读升格窗",
    "窥视审计链",
]

建表 = """
CREATE TABLE IF NOT EXISTS 名空间册 (
  名空间键 TEXT PRIMARY KEY,
  别名 TEXT NOT NULL,
  类型 TEXT NOT NULL DEFAULT '主机',
  说明 TEXT NOT NULL DEFAULT '',
  入册时 TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS 挂载账 (
  挂载号 TEXT PRIMARY KEY,
  名空间键 TEXT NOT NULL,
  源路径 TEXT NOT NULL,
  目标路径 TEXT NOT NULL,
  模式 TEXT NOT NULL DEFAULT 'bind',
  传播 TEXT NOT NULL DEFAULT 'private',
  状态 TEXT NOT NULL DEFAULT '已挂',
  只读 INTEGER NOT NULL DEFAULT 0,
  申请时 TEXT NOT NULL,
  卸载时 TEXT NOT NULL DEFAULT '',
  说明 TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS 忙点闸 (
  忙点号 TEXT PRIMARY KEY,
  挂载号 TEXT NOT NULL,
  占用说明 TEXT NOT NULL DEFAULT '',
  状态 TEXT NOT NULL DEFAULT '占用',
  占用时 TEXT NOT NULL,
  释放时 TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS 空桩 (
  名 TEXT PRIMARY KEY,
  状态 TEXT NOT NULL DEFAULT '空桩'
);
"""


def 初始化库() -> None:
    with 连接() as c:
        c.executescript(建表)
        for n in STUBS:
            c.execute("INSERT OR IGNORE INTO 空桩(名) VALUES (?)", (n,))
        c.commit()
