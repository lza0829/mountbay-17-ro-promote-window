import React, { useEffect, useState } from "react";
import { get, post } from "../api.js";

export default function 传播台() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");
  const load = () => get("/挂载账").then((x) => setRows(x.filter((r) => r.状态 === "已挂"))).catch((e) => setErr(String(e)));
  useEffect(() => { load(); }, []);
  async function 设(挂载号, 传播) {
    try {
      await post(`/mnt/${挂载号}/prop`, { 传播 });
      await load();
    } catch (e) {
      setErr(String(e));
    }
  }
  return (
    <div className="牌">
      <h2>传播台</h2>
      <p>对已挂条目切换 private / shared / slave。</p>
      {err && <p className="bad">{err}</p>}
      <table className="表">
        <thead><tr><th>挂载号</th><th>目标</th><th>当前传播</th><th>操作</th></tr></thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.挂载号}>
              <td className="path">{r.挂载号}</td>
              <td className="path">{r.目标路径}</td>
              <td>{r.传播}</td>
              <td className="行">
                {["private", "shared", "slave"].map((p) => (
                  <button key={p} onClick={() => 设(r.挂载号, p)}>{p}</button>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
