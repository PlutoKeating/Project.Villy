# 完整工作规划 · Roadmap

> 本文档定义 Project.Villy 的完整工作规划，按阶段组织，每阶段包含明确的任务、交付物和依赖关系。

---

## 阶段 0：项目脚手架搭建 🏗️

**目标**：建立规范化的工程目录结构和工作流标准。

| # | 任务 | 状态 |
|---|------|------|
| 0.1 | 创建模块化目录结构 | ✅ |
| 0.2 | 编写 `AGENT.md` 工作流规范 | ✅ |
| 0.3 | 编写 `docs/ARCHITECTURE.md` | ✅ |
| 0.4 | 编写本文件 `docs/ROADMAP.md` | ✅ |
| 0.5 | 各模块 README.md + docs/ 初始化 | ⏳ |
| 0.6 | 根目录 `README.md` 项目总览 | ⏳ |
| 0.7 | 全局 `.gitignore` + 各模块 `.gitignore` | ⏳ |

---

## 阶段 1：硬件逆向工程 🔍 — `hardware/`

**目标**：完整获取硬件资源清单，包括所有 GPIO 引脚定义、通信协议、芯片型号与功能。

| # | 任务 | 交付物 | 依赖 |
|---|------|--------|------|
| 1.1 | 拆机，高清拍摄所有 PCB 正反面 | `hardware/teardown/` 照片 | — |
| 1.2 | 识别并标注所有关键芯片 | `hardware/docs/chip-identification.md` | 1.1 |
| 1.3 | 追踪 GPIO 引脚：SoC → 外设 | `hardware/docs/gpio-map.md` | 1.1 |
| 1.4 | 定位调试接口（UART/JTAG/USB） | `hardware/docs/debug-ports.md` | 1.1 |
| 1.5 | 串口终端接入，抓取启动日志 | `hardware/docs/boot-log.md` | 1.4 |
| 1.6 | 分析传感器通信协议（I2C/SPI/UART） | `hardware/docs/protocols.md` | 1.2 |
| 1.7 | 导出原厂固件分区布局 | `hardware/docs/partition-layout.md` | 1.5 |
| 1.8 | 整理可刷入的 Linux 发行版列表 | `hardware/docs/linux-distros.md` | 1.2 |

---

## 阶段 2：固件与刷写 🔧 — `firmware/`

**目标**：建立完整的刷写工具链，实现从原厂固件到自定义 Linux 的刷写流程。

| # | 任务 | 交付物 | 依赖 |
|---|------|--------|------|
| 2.1 | 引入 Allwinner R16 交叉编译工具链（submodule） | `firmware/submodules/` | 1.2 |
| 2.2 | 引入主线 Linux (sunxi) 源码（submodule） | `firmware/submodules/` | 1.2 |
| 2.3 | 编写内核 `.config` 适配 SDJQR01RR | `firmware/configs/kernel.config` | 2.2 |
| 2.4 | 编写设备树 DTS | `firmware/dts/sdjqr01rr.dts` | 1.3 |
| 2.5 | 构建最小 rootfs（Buildroot） | `firmware/docs/build-guide.md` | 2.1 |
| 2.6 | 刷写流程文档与工具脚本 | `firmware/docs/flashing-guide.md` | 2.5 |
| 2.7 | 实际刷写并记录结果 | `firmware/docs/flashing-log.md` | 2.6 |
| 2.8 | GPIO / I2C / SPI / PWM 驱动验证 | `firmware/docs/driver-validation.md` | 2.7 |

---

## 阶段 3：后端服务 🔌 — `backend/`

**目标**：构建完整的 Flask API 服务、硬件抽象层（HAL）、HMAC 认证体系。

| # | 任务 | 交付物 | 依赖 |
|---|------|--------|------|
| 3.1 | Flask 项目骨架搭建 | `backend/app/` | — |
| 3.2 | HMAC 认证中间件设计实现 | `backend/app/auth/` + `backend/docs/auth-scheme.md` | — |
| 3.3 | API 路由与端点定义 | `backend/app/api/` + `backend/docs/api-reference.md` | 3.1 |
| 3.4 | HAL 硬件抽象层设计 | `backend/app/hal/` | 2.8 |
| 3.5 | 传感器数据采集实现 | `backend/app/hal/sensors/` | 3.4 |
| 3.6 | 电机控制接口实现 | `backend/app/hal/motors/` | 3.4 |
| 3.7 | WebSocket 遥测推送 | `backend/app/api/ws.py` | 3.3 |
| 3.8 | 配置管理与环境变量 | `backend/config/` | — |
| 3.9 | 单元测试 + 集成测试 | `backend/tests/` | 3.3 |

---

## 阶段 4：前端控制面板 🎛️ — `frontend/`

**目标**：构建 React 控制仪表盘，实现传感器可视化、遥控和系统监控。

| # | 任务 | 交付物 | 依赖 |
|---|------|--------|------|
| 4.1 | React + Vite + Tailwind 项目初始化 | `frontend/` | — |
| 4.2 | HMAC 签名请求库封装 | `frontend/src/lib/api.ts` | 3.2 |
| 4.3 | 仪表盘主页面 | `frontend/src/pages/Dashboard.tsx` | 4.2 |
| 4.4 | 遥控控制面板 | `frontend/src/pages/Control.tsx` | 4.2 |
| 4.5 | 传感器实时图表 | `frontend/src/components/SensorChart.tsx` | 3.7 |
| 4.6 | 系统信息与日志页 | `frontend/src/pages/System.tsx` | 4.2 |
| 4.7 | 响应式移动端适配 | 全部组件 | 4.3-4.6 |

---

## 阶段 5：ROS 2 集成评估 🤖 — `ros2/`

**目标**：评估 ROS 2 / micro-ROS 在此硬件上的可行性，做出引入或自研的最终决策。

| # | 任务 | 交付物 | 依赖 |
|---|------|--------|------|
| 5.1 | 256MB RAM 资源预算评估 | `ros2/docs/resource-budget.md` | 2.7 |
| 5.2 | ARMv7 ROS 2 / micro-ROS 兼容性调研 | `ros2/docs/compatibility.md` | 5.1 |
| 5.3 | HAL → ROS 2 桥接方案设计 | `ros2/docs/bridge-design.md` | 3.4, 5.2 |
| 5.4 | **最终决策**：引入 ROS 2 或继续自研 HAL | `ros2/docs/decision.md` | 5.1-5.3 |

---

## 依赖关系图

```
阶段 0 (脚手架)
 │
 ├─→ 阶段 1 (硬件逆向) ──→ 阶段 2 (固件刷写) ──→ 阶段 3 (后端 HAL)
 │                                                    │
 └─→ (并行可启动)                                     ├─→ 阶段 4 (前端)
                                                      │
                                                      └─→ 阶段 5 (ROS 评估)
```

- 阶段 3 / 4 / 5 可在阶段 2 完成前并行开发（使用 mock 硬件）
- 阶段 4 依赖阶段 3 的 API 定义
- 阶段 5 最终决策依赖阶段 3 的 HAL 设计和阶段 2 的实际资源测量

---

*最后更新：2026-08-08*
