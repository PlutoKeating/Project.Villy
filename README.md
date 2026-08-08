<h1 align="center">🤖 Project.Villy</h1>

<p align="center">
  <strong>小米扫地机器人 1 代 → Linux 可编程机器人底盘</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/hardware-Allwinner_R16-orange" alt="Hardware">
  <img src="https://img.shields.io/badge/arch-ARMv7-blue" alt="Architecture">
  <img src="https://img.shields.io/badge/status-Phase_1_侦察-yellow" alt="Status">
  <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="License">
</p>

---

拆掉原厂固件，刷入 Linux，把一台 2016 年的退役扫地机（SDJQR01RR）变成可通过 WiFi 遥控、完全可编程的机器人底盘。比买 TurtleBot 便宜，比从零造简单。

> 架构设计 → [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)　　完整路线图 → [`docs/ROADMAP.md`](docs/ROADMAP.md)　　工作流规范 → [`AGENT.md`](AGENT.md)

---

## 模块

| | 模块 | 职责 |
|---|------|------|
| 🔍 | [`hardware/`](hardware/README.md) | 硬件逆向：GPIO 映射、芯片识别、通信协议分析 |
| 🔧 | [`firmware/`](firmware/README.md) | 固件刷写：交叉编译工具链、内核构建、FEL 刷写 |
| 🔌 | [`backend/`](backend/README.md) | Flask API + HAL 抽象层 + HMAC-SHA256 认证 |
| 🎛️ | [`frontend/`](frontend/README.md) | React 仪表盘 + 遥控面板（Tailwind / Vite） |
| 🤖 | [`ros2/`](ros2/README.md) | ROS 2 / micro-ROS 集成评估（待决策） |

## 技术栈

| 层 | 选型 |
|----|------|
| 后端 | Python 3.14+ / Flask 3.x |
| 认证 | HMAC-SHA256 签名（零外部依赖） |
| 前端 | React 19 / Tailwind CSS 4 / Vite 6 |
| 实时通信 | WebSocket (Flask-Sock) |
| 内核 | 主线 Linux (sunxi) + 设备树 |
| rootfs | Buildroot → Debian armhf |
| 机器人框架 | 自研轻量 HAL（ROS 2 待评估） |

## 参考

- [Valetudo](https://github.com/Hypfer/Valetudo) — 扫地机器人去云端固件
- [Dustcloud](https://github.com/dgiese/dustcloud) — 小米扫地机 MITM 代理
- [linux-sunxi / R16](https://linux-sunxi.org/R16) — 全志 SoC 主线移植

---

> [!IMPORTANT]
> **学习与研究用途声明：** 本项目以学习、互操作性研究和经授权的设备实验为目的发布。它不构成对任何设备进行访问、绕过保护或刷写操作的授权，也不提供适销性、特定用途适用性、数据安全或硬件可恢复性的保证。你只能在自己拥有或已获得明确授权的设备上操作，并须遵守所在地法律和第三方权利。Xiaomi、Roborock、Allwinner 及其他上游项目不为本项目背书。

## 许可

本项目基于 [GNU Affero General Public License v3.0](LICENCE) 发布。包含的第三方组件遵循其各自的许可证。

---

*"旧物新生，从拆开它的那一刻开始。"*
