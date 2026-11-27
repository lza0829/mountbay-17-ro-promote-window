import React, { useEffect, useState } from "react";
import { get } from "../api.js";

export default function 载界验() {
  const [v, setV] = useState(null);
  const [err, setErr] = useState("");
  const load = () => get("/载界验").then(setV).catch((e) => setErr(String(e)));
  useEffect(() => { load(); }, []);
  return (
    <div className="牌">
      <h2>载界验</h2>
      <p>核对名空间、挂载与忙点账是否自洽。</p>
      <div className="行"><button onClick={load}>重新核对</button></div>
      {err && <p className="bad">{err}</p>}
      {v && (
        <>
          <p className={v.valid ? "ok" : "bad"}>{v.valid ? "通过" : "未过"} · {v.说明}</p>
          <div className="格网">
            <div className="格"><span className="静">名空间</span><b>{v.名空间数}</b></div>
            <div className="格"><span className="静">已挂</span><b>{v.已挂数}</b></div>
            <div className="格"><span className="静">忙点</span><b>{v.忙点数}</b></div>
          </div>
        </>
      )}
    </div>
  );
}
