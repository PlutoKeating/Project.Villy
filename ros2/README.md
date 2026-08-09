# ROS 2 集成评估

> 本模块评估将 ROS 2 / micro-ROS 引入 Project.Villy 的可行性。
> **当前状态：评估中，待阶段 2 完成后做最终决策。**

## 评估维度

| 维度 | 约束 |
|------|------|
| CPU | Allwinner A33, 4× Cortex-A7 @ 1.2GHz |
| RAM | 256 MB DDR3（可用约 192MB 给应用层） |
| 存储 | 512 MB NAND（可用约 256MB 给 rootfs + ROS） |
| 架构 | ARMv7 (armhf) |
| 实时性 | 无实时内核补丁 |

## 待调研

- ROS 2 Humble / Jazzy armhf 预编译包可用性
- micro-ROS 在 ARMv7 + Buildroot 上的移植难度
- 自研轻量 HAL vs ROS 2 的维护成本对比

## 快速入口

| 文档 | 内容 |
|------|------|
| [资源预算](docs/resource-budget.md) | RAM / Flash 占用预估 |
| [兼容性调研](docs/compatibility.md) | ROS 2 / micro-ROS ARMv7 支持 |
| [桥接方案](docs/bridge-design.md) | HAL → ROS 2 桥接架构 |
| [最终决策](docs/decision.md) | 引入 ROS 2 或继续自研 HAL |

---

*本模块的最终决策将直接影响 `backend/app/hal/` 的架构方向。*
