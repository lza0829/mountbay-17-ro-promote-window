import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import 入口 from "./pages/入口.jsx";
import 名空间册 from "./pages/名空间册.jsx";
import 挂载账 from "./pages/挂载账.jsx";
import 传播台 from "./pages/传播台.jsx";
import 忙点闸 from "./pages/忙点闸.jsx";
import 载界验 from "./pages/载界验.jsx";

const 链 = [
  ["/", "入口"],
  ["/名空间册", "名空间册"],
  ["/挂载账", "挂载账"],
  ["/传播台", "传播台"],
  ["/忙点闸", "忙点闸"],
  ["/载界验", "载界验"],
];

export default function App() {
  return (
    <div className="壳">
      <aside className="侧轨">
        <div>
          <div className="侧英">Mountbay · OS</div>
          <h1 className="侧名">载<span>界</span></h1>
          <p className="侧骨">挂载申请后设传播；忙点占用时卸载失败闭，释放后再卸；名空间可见性可核对。</p>
        </div>
        <nav className="侧导">
          {链.map(([to, l]) => (
            <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => (isActive ? "亮" : "")}>
              {l}
            </NavLink>
          ))}
        </nav>
        <div className="侧脚">SYS · KERNEL · :7200</div>
      </aside>
      <main className="主">
        <Routes>
          <Route path="/" element={<入口 />} />
          <Route path="/名空间册" element={<名空间册 />} />
          <Route path="/挂载账" element={<挂载账 />} />
          <Route path="/传播台" element={<传播台 />} />
          <Route path="/忙点闸" element={<忙点闸 />} />
          <Route path="/载界验" element={<载界验 />} />
        </Routes>
      </main>
    </div>
  );
}
