import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { get, post } from "../api.js";

export default function 入口() {
  const [ov, setOv] = useState(null);
  const [msg, setMsg] = useState("");
  const refresh = () => get("/总览").then(setOv).catch((e) => setMsg(String(e)));
  useEffect(() => { refresh(); }, []);

  async function 一键演示() {
    setMsg("跑演示…");
    try {
      const ns = await post("/演示/入册", { 别名: "演示主机名空间", 类型: "主机" });
      const m = await post("/演示/申请挂载", {
        名空间键: ns.名空间键,
        源路径: "/var/demo",
        目标路径: "/mnt/demo",
        传播: "private",
      });
      const b = await post("/演示/占忙点", { 挂载号: m.挂载号, 占用说明: "演示读占用" });
      try {
        await post(`/mnt/${m.挂载号}/umount`);
        setMsg("异常：忙点下卸载竟成功");
        return;
      } catch (_) {}
      await post(`/busy/${b.忙点号}/release`);
      await post(`/mnt/${m.挂载号}/umount`);
      const v = await get("/载界验");
      setMsg(v.valid ? "演示闭环通过：占忙拒卸 → 释放后卸载。" : "演示完成但载界验未过");
      refresh();
    } catch (e) {
      setMsg(String(e));
    }
  }

  return (
    <div>
      <div className="牌">
        <h2>载界入口</h2>
        <p>先入册名空间，再申请挂载；忙点占用时卸载必须失败闭。</p>
        <div className="行">
          <button className="主钮" onClick={一键演示}>演练挂载闭环</button>
          <Link className="钮" to="/名空间册">去名空间册</Link>
        </div>
        {msg && <p className="静">{msg}</p>}
      </div>
      {ov && (
        <div className="格网">
          <div className="格"><span className="静">名空间</span><b>{ov.名空间数}</b></div>
          <div className="格"><span className="静">已挂</span><b>{ov.已挂数}</b></div>
          <div className="格"><span className="静">忙点</span><b>{ov.忙点数}</b></div>
        </div>
      )}
    </div>
  );
}
