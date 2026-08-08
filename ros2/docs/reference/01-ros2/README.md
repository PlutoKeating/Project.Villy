# 4.1 ROS 2 在 ARMv7 的可行性

---

## ROS 2 发行版选择

| 发行版 | 代号 | 状态 | armhf 支持 |
|--------|------|------|-----------|
| ROS 2 Humble | Humble Hawksbill | LTS (2027) | ⚠️ 仅有源码 |
| ROS 2 Iron | Iron Irwini | 非 LTS | ❌ 终止 |
| ROS 2 Jazzy | Jazzy Jalisco | LTS (2029) | ❌ 仅 amd64/arm64 |
| ROS 2 Rolling | Rolling Ridley | 滚动 | ⚠️ 源码编译 |

**结论**：没有 ROS 2 发行版为 armhf 提供官方预编译包。

---

## 源码编译 ROS 2 Humble 评估

### 最低系统要求

| 组件 | 官方要求 | R16 实际 |
|------|---------|----------|
| RAM | 4 GB | 256 MB ❌ |
| 磁盘 | 20 GB | 512 MB ❌ |
| CPU 核心 | 4+ | 4 ✅ |
| 架构 | amd64/arm64 | armhf ❌ |

官方要求的 RAM/磁盘远超 R16 硬件能力。

### 交叉编译方案

理论上可交叉编译 ROS 2 到 armhf：
```bash
# 使用 ROS 2 交叉编译工具
# 参考：https://docs.ros.org/en/humble/How-To-Guides/Cross-compilation.html
```
但实际成功率低，依赖链复杂且易断裂。

---

## 实际可运行的 ROS 2 方案

### 方案一：跨设备 ROS 2

```
R16 (传感器/执行器)    远程 PC (ROS 2)
   │                      │
   │ UDP/WebSocket ───────│ ros2 run ...
   │ 简单数据帧           │ SLAM / Navigation
```

机器人底盘运行轻量级数据采集程序，通过 UDP 或 WebSocket 发送给远程 PC 上的 ROS 2 节点。

### 方案二：micro-ROS Agent

```
R16 (micro-ROS Client)    Linux PC (micro-ROS Agent + ROS 2)
   │                           │
   │ DDS-XRCE ────────────────│ ros2 run ...
   │                           │
```

micro-ROS Client 运行在 R16 上，通过 DDS-XRCE 协议与 PC 上的 micro-ROS Agent 通信。

---

## 社区案例

### 成功案例

- **Raspberry Pi 3/4 (armhf/arm64)**：有社区成功运行 ROS 2 的案例，但 Pi 4 有 4GB RAM
- **micro-ROS on STM32**：大量成功案例，但面向 MCU 而非 MPU

### 失败/困难案例

- **Snap micro-ROS-agent on arm64**：用户报告 `micro-ros-agent` snap 在 ARM 上不可用
- **ARM 交叉编译失败**：fishros 论坛报告 ROS 2 Galactic 在 ARM 上找不到中间件

---

## 对 Project.Villy 的建议

| 优先级 | 行动 |
|--------|------|
| P0 | 继续推进自研 HAL（`backend/app/hal/`） |
| P1 | 实现 WebSocket 遥测 → 可对接远程 ROS 2 |
| P2 | 评估 micro-ROS Client 在 Buildroot 上的移植 |
| P3 | 等待 ROS 2 官方 armhf 支持或硬件升级后重新评估 |

---

## 参考资源

- ROS 2 交叉编译指南：https://docs.ros.org/en/humble/How-To-Guides/Cross-compilation.html
- ROS 2 支持的架构：https://www.ros.org/reps/rep-2000.html
- micro-ROS 官方：https://micro.ros.org/
- ROS Discourse ARM 讨论：https://discourse.ros.org/
- Raspberry Pi ROS 2 经验：https://robotics.stackexchange.com/
