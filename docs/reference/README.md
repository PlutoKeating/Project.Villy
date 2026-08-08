# 小米扫地机器人 SDJQR01RR 逆向工程参考手册

> **Project.Villy** — 旧物新生，从拆开它的那一刻开始。

本手册为 Project.Villy 的**完整技术参考文档**，涵盖硬件逆向、固件刷写、软件架构、ROS 2 评估和社区资源五大领域。所有内容基于网络调研和开源社区最佳实践编撰，为后期开发提供系统化参考。

---

## 📚 文档导航

| 章节 | 路径 | 内容 |
|------|------|------|
| **第 1 章：硬件逆向** | [`hardware/docs/reference/`](../hardware/docs/reference/) | SoC 芯片识别、PCB 分析、GPIO 映射、调试接口、通信协议、传感器、电机驱动、电源管理、WiFi 模块 |
| **第 2 章：固件与刷写** | [`firmware/docs/reference/`](../firmware/docs/reference/) | sunxi 生态、FEL 刷写、交叉编译、内核配置、Buildroot/Debian rootfs、Valetudo/Dustcloud 生态、U-Boot、固件提取 |
| **第 3 章：软件架构** | [`backend/docs/reference/`](../backend/docs/reference/) + [`frontend/docs/reference/`](../frontend/docs/reference/) | HAL 设计、API 安全认证、WebSocket 遥测、React 仪表盘 |
| **第 4 章：ROS 2 评估** | [`ros2/docs/reference/`](../ros2/docs/reference/) | ROS 2 ARMv7 兼容性、micro-ROS 深度调研、替代框架对比 |
| **第 5 章：社区资源** | [`docs/reference/community/`](../docs/reference/community/) | GitHub 项目索引、论坛社区、芯片数据手册、博客文章 |

---

## 🔑 关键术语速查

| 术语 | 全称 / 说明 |
|------|-------------|
| **SDJQR01RR** | 小米扫地机器人 1 代国行型号 |
| **R16** | Allwinner 全志 R16 SoC（4×Cortex-A7, Mali400MP2） |
| **FEL** | Failsafe Engine Loader — Allwinner BootROM USB 刷写模式 |
| **sunxi** | Allwinner SoC 的 Linux 主线移植项目 |
| **sunxi-fel** | FEL 模式 USB 通信/刷写工具 |
| **Valetudo** | 扫地机器人去云端开源固件（Go/Node.js） |
| **Dustcloud** | 小米智能家居设备 MITM 代理 + 逆向工程 |
| **Dustbuilder** | 在线定制 root 固件构建工具 |
| **DTS** | Device Tree Source — Linux 设备树源码 |
| **DTB** | Device Tree Blob — 编译后的设备树 |
| **LDS** | Laser Distance Sensor — 激光测距传感器 |
| **HAL** | Hardware Abstraction Layer — 硬件抽象层 |

---

## ⚠️ 重要声明

> 本手册所有内容均来自公开网络资源、开源社区文档和个人研究成果的汇总，仅供学习与研究参考。所有操作请在自有设备上进行，遵守当地法律。

---

*最后更新：2026-08-09*
