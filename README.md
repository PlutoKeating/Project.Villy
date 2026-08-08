<h1 align="center">🤖 Project.Villy</h1>

<p align="center">
  <strong>退役扫地机器人 → Linux 可编程机器人底盘</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/hardware-Allwinner_R16-orange" alt="Hardware">
  <img src="https://img.shields.io/badge/arch-ARMv7-blue" alt="Architecture">
  <img src="https://img.shields.io/badge/OS-Linux_(Buildroot)-lightgrey" alt="OS">
  <img src="https://img.shields.io/badge/status-Phase_1_侦察-yellow" alt="Status">
  <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="License">
</p>

---

## 一句话

**小米扫地机器人 1 代（SDJQR01RR），拆掉原厂固件，刷入 Linux，变成一台可通过 WiFi 遥控、可编程的机器人底盘。**

---

## 为什么做这个？

2016 年的小米扫地机器人 1 代，在今天已经无法正常服役。但它的硬件底子并不差——全志 R16 四核处理器、LDS 激光雷达、超声波、IMU、4 个 BLDC 电机、5200mAh 电池。

与其扔进垃圾桶，不如把它变成一台 **完全开源、可编程、可遥控的机器人开发平台**。比买一台 TurtleBot 便宜，比从零造一台简单。

> **"你不需要买一台昂贵的机器人来学习 ROS——你只需要一台退役的扫地机。"**

---

## 目标设备

| 规格 | 详情 |
|------|------|
| **产品** | 米家扫地机器人 / Mi Robot Vacuum |
| **型号** | SDJQR01RR（STYTJ01YM） |
| **CPU** | Allwinner R16，四核 ARM Cortex-A7 @ 1.2GHz |
| **RAM** | 256 MB DDR3 |
| **存储** | 512 MB NAND Flash |
| **WiFi** | Realtek RTL8189ETV（2.4GHz） |
| **电池** | 5200 mAh / 14.4V |
| **原厂系统** | 定制 Linux（ARMv7，Buildroot 系） |

### 传感器与执行器

| 组件 | 规格 |
|------|------|
| 🔴 LDS 激光雷达 | 360° 扫描，SLAM 导航核心 |
| 📡 超声波雷达 | 前方障碍物检测 |
| ⬇️ 悬崖传感器 | 4 组红外传感器 |
| 🧭 IMU | 六轴陀螺仪 + 加速度计 |
| 🔄 里程计 | 2 组磁编码器 |
| ⚙️ 驱动轮 ×2 | BLDC 电机 + 编码器 |
| 🧹 主刷 / 边刷 / 风机 | 各 1 个 BLDC 电机 |

---

## 路线图

> [!NOTE]
> 当前处于 **第一阶段：侦察**。实物已就位，待拆机。

### 🔍 第一阶段 — 侦察

- [ ] 拆机，全方位拍摄 PCB
- [ ] 识别芯片：SoC、RAM、Flash、WiFi、电机驱动、传感器接口
- [ ] 定位调试触点（UART / JTAG / USB）
- [ ] 串口终端接入
- [ ] 导出固件 & 启动日志

### 🧠 第二阶段 — 理解原厂系统

- [ ] 分析启动流程（bootloader → kernel → init）
- [ ] 查明电机控制协议
- [ ] 逆向传感器数据流
- [ ] 映射 GPIO 引脚
- [ ] 理解 WiFi / 云端通信协议

### 🔓 第三阶段 — Root & 定制固件

- [ ] 实现持久 root 访问
- [ ] 评估 Valetudo、Dustcloud 等社区方案
- [ ] 为 Allwinner R16 交叉编译现代 Linux 内核
- [ ] 构建最小 rootfs（Buildroot / Debian armhf）
- [ ] 从 SD 卡启动自定义 Linux

### 🤖 第四阶段 — 机器人底盘平台

- [ ] 编写传感器 & 电机内核驱动
- [ ] 硬件抽象层（HAL）—— 统一 API
- [ ] WiFi 遥控（WebSocket / HTTP API）
- [ ] ROS 2 集成
- [ ] 基于 LDS 的 SLAM 演示
- [ ] 自主导航

### 🚀 第五阶段 — 打磨 & 发布

- [ ] 3D 打印扩展支架
- [ ] Web 控制面板
- [ ] 完整文档 & 构建指南
- [ ] 全部开源

---

## 仓库结构

```
Project.Villy/
├── README.md            # ← 你在这里
├── docs/                # 文档
│   ├── hardware/        #   硬件：PCB 照片、芯片手册、引脚定义
│   ├── firmware/        #   固件：启动流程、逆向分析笔记
│   └── build/           #   构建：交叉编译指南
├── firmware/            # 定制固件 & 内核补丁
├── hal/                 # 硬件抽象层
├── software/            # 控制软件（API + Web）
├── ros2/                # ROS 2 包
├── 3d-models/           # 3D 打印模型
└── tools/               # 调试工具
```

---

## 社区参考

- [Valetudo](https://github.com/Hypfer/Valetudo) — 扫地机器人去云端固件，支持多品牌
- [Dustcloud](https://github.com/dgiese/dustcloud) — 小米扫地机中间人代理
- [Allwinner R16 @ linux-sunxi](https://linux-sunxi.org/R16) — 全志 SoC 主线 Linux 移植社区
- [Roborock Firmware Analysis](https://github.com/ghoost82/roborock-firmware) — 石头固件逆向分析

---

> [!IMPORTANT]
> **学习与研究用途声明：** 本项目以学习、互操作性研究和经授权的设备实验为目的发布。它不构成对任何设备进行访问、绕过保护或刷写操作的授权，也不提供适销性、特定用途适用性、数据安全或硬件可恢复性的保证。你只能在自己拥有或已获得明确授权的设备上操作，并须遵守所在地法律和第三方权利。小米、Roborock、Allwinner 及其他上游项目不为本项目背书。

---

## 许可

本项目基于 [GNU Affero General Public License v3.0](LICENCE) 发布。

包含的第三方组件遵循其各自的许可证。

---

*"旧物新生，从拆开它的那一刻开始。"*
