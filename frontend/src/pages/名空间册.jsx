import React, { useEffect, useState } from "react";
import { get, post } from "../api.js";

export default function 名空间册() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");
  const load = () => get("/名空间册").then(setRows).catch((e) => setErr(String(e)));
  useEffect(() => { load(); }, []);
  return (
    <div className="牌">
      <h2>名空间册</h2>
      <p>登记可挂载的名空间边界（主机或模拟容器）。</p>
      <div className="行">
        <button className="主钮" onClick={() => post("/演示/入册", { 别名: "演示名空间" }).then(load).catch((e) => setErr(String(e)))}>
          登记演示名空间
        </button>
      </div>
      {err && <p className="bad">{err}</p>}
      <table className="表">
        <thead><tr><th>键</th><th>别名</th><th>类型</th><th>入册时</th></tr></thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.名空间键}><td className="path">{r.名空间键}</td><td>{r.别名}</td><td>{r.类型}</td><td className="静">{r.入册时}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
