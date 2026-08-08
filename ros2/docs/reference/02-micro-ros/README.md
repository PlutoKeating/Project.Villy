# 4.2 micro-ROS 深度调研

> micro-ROS 将 ROS 2 的核心概念（节点、发布/订阅、参数、生命周期）带到资源受限的嵌入式系统。

---

## micro-ROS 概述

**官网**：https://micro.ros.org/

micro-ROS 是 ROS 2 的轻量级变体，专为 MCU 级嵌入式系统设计：

- **目标平台**：FreeRTOS、Zephyr、NuttX、Arduino、Linux（嵌入式）
- **中间件**：Micro XRCE-DDS（eProsima 开发）
- **传输层**：UART、UDP、TCP、USB CDC
- **内存占用**：客户端 ~20-50KB RAM（取决于节点数量）

---

## 架构

```
┌──────────────────────────────────────────────────┐
│              嵌入式设备 (R16)                       │
│                                                  │
│  ┌──────────────────────┐                        │
│  │  传感器节点           │                        │
│  │  micro-ROS Client    │ ← DDS-XRCE(UART/UDP)   │
│  │  (C 代码, tiny)       │                        │
│  └──────────┬───────────┘                        │
│             │                                     │
└─────────────┼─────────────────────────────────────┘
              │
              │  DDS-XRCE Protocol
              │
┌─────────────┼─────────────────────────────────────┐
│  PC / SBC                                       │
│             ▼                                    │
│  ┌──────────────────────┐                        │
│  │  micro-ROS Agent     │                        │
│  │  (Python/C, 中等)     │                        │
│  └──────────┬───────────┘                        │
│             │                                     │
│             ▼                                     │
│  ┌──────────────────────┐                        │
│  │  ROS 2 (完整)        │                        │
│  │  DDS (Fast-DDS)      │                        │
│  └──────────────────────┘                        │
└──────────────────────────────────────────────────┘
```

---

## 关键组件

### micro-ROS Client

- 运行在嵌入式设备上
- 用 C 语言实现，编译为静态库
- 链接到传感器/执行器代码
- 通过 DDS-XRCE 与 Agent 通信

### micro-ROS Agent

- 运行在 PC/SBC 上（需要 ROS 2）
- 桥接 micro-ROS Client 和完整的 ROS 2 DDS 网络
- 支持多 Client 同时连接

### DDS-XRCE (DDS for eXtremely Resource Constrained Environments)

- OMG 标准协议
- 客户端-服务器模型（vs DDS 的 P2P 模型）
- 极低内存占用
- 支持可靠/尽力传输

---

## 在 R16 上的适用性

### 可行性

| 维度 | 分析 |
|------|------|
| **协议** | DDS-XRCE over UDP 完全可行 |
| **Agent** | R16 可运行 micro-ROS Agent（Linux 进程） |
| **Client** | 如仅做数据采集，Client 可运行在更小的 MCU |
| **内存** | micro-ROS Client ~50KB，远低于 ROS 2 完整栈 |

### 推荐的 R16 集成方案

```
方案：R16 作为 micro-ROS Agent + 传感器中间件

R16 上运行：
  - Linux (Buildroot/Debian)
  - 自研 HAL（传感器数据采集 + 电机控制）
  - micro-ROS Agent（可选，桥接到远程 ROS 2）
  - WebSocket 服务器（项目已有的遥测方案）
```

---

## micro-ROS 社区案例

| 项目 | 平台 | 说明 |
|------|------|------|
| micro-ROS Thumper Demo | Olimex STM32-E407 | 6 轮移动机器人 |
| Luos + micro-ROS | STM32 | 分布式电机控制 |
| ESP32 + micro-ROS | ESP32 | WiFi 机器人遥测 |

---

## 参考资源

- 官方文档：https://micro.ros.org/docs/
- GitHub：https://github.com/micro-ROS
- eProsima Micro XRCE-DDS：https://github.com/eProsima/Micro-XRCE-DDS
- ROS Discourse（micro-ROS 板块）：https://discourse.ros.org/
- micro-ROS 内存分析：https://micro.ros.org/docs/concepts/middleware/micro_xrce_dds/
