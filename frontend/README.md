# Frontend 前端控制面板

> 本模块提供机器人的 Web 图形化控制与观测仪表盘。

## 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 框架 | React 19 | 生态成熟，组件丰富 |
| 构建 | Vite 6 | 极速 HMR，TypeScript 原生支持 |
| 样式 | Tailwind CSS 4 | 响应式布局，mobile-first |
| 路由 | React Router 7 | 声明式路由 |
| 图表 | Recharts | 轻量级 React 图表库 |
| HTTP | 封装 `fetch` + HMAC 签名 | 零额外依赖 |

## 目录结构

```
frontend/
├── README.md
├── docs/
│   └── components.md       # 组件树与数据流
├── src/
│   ├── main.tsx            # 入口
│   ├── App.tsx             # 路由定义
│   ├── pages/
│   │   ├── Dashboard.tsx   # 仪表盘主页
│   │   ├── Control.tsx     # 遥控面板
│   │   └── System.tsx      # 系统信息
│   ├── components/
│   │   ├── Layout.tsx      # 全局布局（导航栏）
│   │   ├── SensorPanel.tsx # 传感器面板
│   │   ├── MotorControl.tsx# 电机控制
│   │   └── SensorChart.tsx # 实时传感器图表
│   ├── hooks/
│   │   └── useTelemetry.ts # WebSocket 遥测 hook
│   └── lib/
│       └── api.ts          # HMAC 签名请求封装
├── public/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── .gitignore
```

## 页面路由

| 路径 | 页面 | 功能 |
|------|------|------|
| `/` | Dashboard | 状态总览、电池、传感器一览 |
| `/control` | Control | 摇杆/方向键遥控 |
| `/system` | System | 系统信息、日志 |

## 开发运行

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

生产构建后会作为静态文件由 Flask 后端托管（`backend/app/` 配置静态文件路径）。

---

> 所有操作记录严格遵循 [AGENT.md](../../AGENT.md) 规范。
