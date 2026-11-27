import React, { useEffect, useState } from "react";
import { get, post } from "../api.js";

export default function 忙点闸() {
  const [busy, setBusy] = useState([]);
  const [mounts, setMounts] = useState([]);
  const [msg, setMsg] = useState("");
  const load = async () => {
    setBusy(await get("/忙点闸"));
    setMounts((await get("/挂载账")).filter((m) => m.状态 === "已挂"));
  };
  useEffect(() => { load().catch((e) => setMsg(String(e))); }, []);

  async function 占(挂载号) {
    try {
      await post("/演示/占忙点", { 挂载号, 占用说明: "页面占用" });
      setMsg("已占忙点");
      await load();
    } catch (e) {
      setMsg(String(e));
    }
  }
  async function 试卸(挂载号) {
    try {
      await post(`/mnt/${挂载号}/umount`);
      setMsg("卸载成功");
      await load();
    } catch (e) {
      setMsg("卸载被拒（预期若忙点占用）：" + String(e));
    }
  }
  async function 释(忙点号) {
    await post(`/busy/${忙点号}/release`);
    await load();
  }

  return (
    <div className="牌">
      <h2>忙点闸</h2>
      <p>占用中禁止卸载；释放后允许卸载。</p>
      {msg && <p className="静">{msg}</p>}
      <h3>已挂</h3>
      <table className="表">
        <thead><tr><th>挂载号</th><th>目标</th><th>操作</th></tr></thead>
        <tbody>
          {mounts.map((m) => (
            <tr key={m.挂载号}>
              <td className="path">{m.挂载号}</td>
              <td className="path">{m.目标路径}</td>
              <td className="行">
                <button onClick={() => 占(m.挂载号)}>占忙点</button>
                <button onClick={() => 试卸(m.挂载号)}>尝试卸载</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>忙点</h3>
      <table className="表">
        <thead><tr><th>忙点号</th><th>挂载号</th><th>状态</th><th>操作</th></tr></thead>
        <tbody>
          {busy.map((b) => (
            <tr key={b.忙点号}>
              <td className="path">{b.忙点号}</td>
              <td className="path">{b.挂载号}</td>
              <td>{b.状态}</td>
              <td>{b.状态 === "占用" && <button onClick={() => 释(b.忙点号)}>释放</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
