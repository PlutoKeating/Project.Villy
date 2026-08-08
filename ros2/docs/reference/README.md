# 第 4 章：ROS 2 集成评估参考

> 评估在 Allwinner R16 (256MB RAM, ARMv7) 上引入 ROS 2 / micro-ROS 的可行性。

---

## 4.1 子章节导航

| 编号 | 文档 | 内容 |
|------|------|------|
| 4.1 | [ROS 2 在 ARMv7 的可行性](./01-ros2/README.md) | 预编译包、源码编译、资源需求 |
| 4.2 | [micro-ROS 深度调研](./02-micro-ros/README.md) | MCU 级 ROS 2、DDS 中间件 |
| 4.3 | [替代框架对比](./03-alternatives/README.md) | 轻量框架对比与自研 HAL 决策 |

---

## 4.2 核心约束

| 维度 | 约束值 | 影响 |
|------|--------|------|
| RAM | 256 MB（可用 ~192MB） | ROS 2 基础栈需 ~50-80MB |
| 存储 | 512 MB NAND（可用 ~256MB） | ROS 2 完整安装 ~200MB+ |
| CPU | 4×Cortex-A7 @ 1.2GHz | DDS 发现协议有一定开销 |
| 架构 | ARMv7 (armhf) | 预编译包稀缺，需源码编译 |
| 实时性 | 无 PREEMPT_RT | 非实时调度 |

---

## 4.3 快速结论

> **当前推荐：自研轻量 HAL（项目已有设计），等待 micro-ROS ARMv7 生态成熟后再评估引入。**

理由：
1. ROS 2 armhf 预编译包极少，源码编译耗时长且易失败
2. 256MB RAM 勉强可运行 ROS 2 最小系统，但剩余空间不足以运行 SLAM 等重负载
3. micro-ROS 主要面向 MCU（STM32/ESP32），在 ARMv7 MPU 上的支持有限
4. 自研 HAL 已覆盖核心需求（电机控制、传感器采集、WebSocket 遥测）

---

*下一节：[4.1 ROS 2 在 ARMv7 的可行性](./01-ros2/README.md)*
