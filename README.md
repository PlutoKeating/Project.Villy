<h1 align="center">🤖 Project.Villy</h1>

<p align="center">
  <strong>退役扫地机器人 → Linux 可编程机器人底盘</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/hardware-Allwinner_R16-orange" alt="Hardware">
  <img src="https://img.shields.io/badge/arch-ARMv7-blue" alt="Architecture">
  <img src="https://img.shields.io/badge/status-Phase_1_侦察-yellow" alt="Status">
  <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="License">
</p>

---

## 一句话

**小米扫地机器人 1 代（SDJQR01RR），拆掉原厂固件，刷入 Linux，变成可通过 WiFi 遥控、可编程的机器人底盘。**

---

## 模块索引

| 模块 | 职责 | 入口 |
|------|------|------|
| 🔍 `hardware/` | 硬件逆向、GPIO 映射、协议分析 | [`hardware/README.md`](hardware/README.md) |
| 🔧 `firmware/` | 交叉编译工具链、内核构建、刷写流程 | [`firmware/README.md`](firmware/README.md) |
| 🔌 `backend/` | Flask API、HAL 抽象层、HMAC 认证 | [`backend/README.md`](backend/README.md) |
| 🎛️ `frontend/` | React 仪表盘、遥控面板、传感器可视化 | [`frontend/README.md`](frontend/README.md) |
| 🤖 `ros2/` | ROS 2 / micro-ROS 集成评估（待决策） | [`ros2/README.md`](ros2/README.md) |

---

## 工作规划

完整路线图见 [`docs/ROADMAP.md`](docs/ROADMAP.md)，架构设计见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)。

### 当前阶段：侦察 & 脚手架

- ⏳ 硬件拆机与 PCB 分析
- ✅ 项目工程化脚手架搭建
- ⏳ 调试串口接入
- ⏳ 原厂固件提取

### 技术栈总览

| 层 | 选型 |
|----|------|
| 后端 API | Python 3.14+ / Flask 3.x |
| 认证 | HMAC-SHA256 签名 |
| 前端 | React 19 / Tailwind CSS 4 / Vite 6 |
| 实时通信 | WebSocket (Flask-Sock) |
| 内核 | 主线 Linux (sunxi) + 设备树 |
| rootfs | Buildroot → Debian armhf |
| 机器人框架 | 自研 HAL（ROS 2 待评估） |

---

## 社区参考

- [Valetudo](https://github.com/Hypfer/Valetudo) — 扫地机器人去云端固件
- [Dustcloud](https://github.com/dgiese/dustcloud) — 小米扫地机中间人代理
- [Allwinner R16 @ linux-sunxi](https://linux-sunxi.org/R16) — 全志 SoC 主线移植社区

---

> [!IMPORTANT]
> **学习与研究用途声明：** 本项目以学习、互操作性研究和经授权的设备实验为目的发布。它不构成对任何设备进行访问、绕过保护或刷写操作的授权，也不提供适销性、特定用途适用性、数据安全或硬件可恢复性的保证。你只能在自己拥有或已获得明确授权的设备上操作，并须遵守所在地法律和第三方权利。Xiaomi、Roborock、Allwinner 及其他上游项目不为本项目背书。

---

## 许可

本项目基于 [GNU Affero General Public License v3.0](LICENCE) 发布。包含的第三方组件遵循其各自的许可证。

---

## 工作流规范

所有贡献者必须遵守 [`AGENT.md`](AGENT.md) 中定义的工程化工作流程。

---

*"旧物新生，从拆开它的那一刻开始。"*
