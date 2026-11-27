import React, { useEffect, useState } from "react";
import { get, post } from "../api.js";

export default function 挂载账() {
  const [rows, setRows] = useState([]);
  const [ns, setNs] = useState([]);
  const [err, setErr] = useState("");
  const load = async () => {
    setNs(await get("/名空间册"));
    setRows(await get("/挂载账"));
  };
  useEffect(() => { load().catch((e) => setErr(String(e))); }, []);
  async function 申请() {
    try {
      let list = ns;
      if (!list.length) {
        const n = await post("/演示/入册", { 别名: "自动名空间" });
        list = [n];
        setNs(list);
      }
      await post("/演示/申请挂载", {
        名空间键: list[0].名空间键,
        源路径: "/var/demo",
        目标路径: "/mnt/demo",
        传播: "private",
      });
      await load();
    } catch (e) {
      setErr(String(e));
    }
  }
  return (
    <div className="牌">
      <h2>挂载账</h2>
      <p>源路径绑定到目标路径；状态为已挂 / 已卸。</p>
      <div className="行"><button className="主钮" onClick={申请}>申请演示挂载</button></div>
      {err && <p className="bad">{err}</p>}
      <table className="表">
        <thead><tr><th>挂载号</th><th>名空间</th><th>源</th><th>目标</th><th>传播</th><th>状态</th></tr></thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.挂载号}>
              <td className="path">{r.挂载号}</td>
              <td className="path">{r.名空间键}</td>
              <td className="path">{r.源路径}</td>
              <td className="path">{r.目标路径}</td>
              <td>{r.传播}</td>
              <td>{r.状态}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
