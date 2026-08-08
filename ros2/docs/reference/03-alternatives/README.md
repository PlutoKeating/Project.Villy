# 4.3 替代框架对比与最终决策

> 在 ROS 2 不可行的情况下，评估替代的机器人框架。

---

## 候选框架对比

| 框架 | 类型 | RAM 需求 | ARMv7 | ROS 兼容 | 学习曲线 | 适合 Villy? |
|------|------|---------|-------|----------|---------|------------|
| **自研 HAL (当前)** | 定制 | ~5MB | ✅ | 需桥接 | 低 | ✅ 最佳 |
| ROS 2 | 完整框架 | ~80MB+ | ❌ | ✅ 原生 | 高 | ❌ |
| micro-ROS | 轻量 ROS | ~50KB | ✅ | ✅ (需Agent) | 中 | ⚠️ 部分 |
| RobotWebTools | Web | ~20MB | ✅ | ✅ | 中 | ⚠️ |
| MRPT | 库集合 | ~30MB | ✅ | 可选 | 高 | ⚠️ |
| Player/Stage | 旧框架 | ~10MB | ✅ | ❌ | 低 | ❌ 已停维 |
| YARP | 中间件 | ~20MB | ✅ | ❌ | 中 | ⚠️ |

---

## 推荐架构：自研 HAL + 可桥接

```
┌──────────────────────────────────────────────────────┐
│                   R16 本地                            │
│                                                      │
│  ┌──────────────────────┐    ┌─────────────────────┐ │
│  │   自研 HAL            │    │   WebSocket Server  │ │
│  │   (Python/C)          │◄──►│   (Flask-Sock)      │ │
│  │                      │    │                     │ │
│  │ • SensorInterface    │    │ • /ws/telemetry     │ │
│  │ • MotorInterface     │    │ • JSON 帧格式        │ │
│  │ • GpioController     │    │ • 双向通信           │ │
│  └──────┬───────────────┘    └────────┬────────────┘ │
│         │                             │              │
│         │ 直接操作                     │ 网络         │
│         │ /sys/class/gpio             │              │
│         │ /dev/i2c-*                  │              │
│         │ /dev/ttyS*                  │              │
└─────────┼─────────────────────────────┼──────────────┘
          │                             │
          ▼                             ▼
    ┌──────────┐              ┌─────────────────────┐
    │  硬件     │              │  远程 PC / 云端      │
    │ GPIO/I²C │              │                     │
    │ UART/SPI │              │  可选桥接层：         │
    └──────────┘              │  • ROS 2 rosbridge   │
                              │  • MQTT Broker       │
                              │  • REST API          │
                              └─────────────────────┘
```

---

## 自研 HAL 设计原则

### 1. 极简接口

每个传感器/执行器暴露最少的方法：

```python
class MotorInterface:
    def set_speed(self, left: int, right: int) -> None: ...
    def stop(self) -> None: ...
    def get_odometry(self) -> tuple[int, int]: ...

class LidarInterface:
    def start_scan(self) -> None: ...
    def get_scan(self) -> list[float]: ...

class ImuInterface:
    def read(self) -> dict: ...
```

### 2. 外部可桥接

通过 WebSocket 暴露的 JSON 帧格式可轻松桥接到 ROS 2（通过 `rosbridge_suite` 或自定义桥接节点）：

```python
# WebSocket 遥测帧 → ROS 2 桥接（PC 端）
# rosrun rosbridge_server rosbridge_websocket
# → 自动将 JSON 帧转换为 ROS 2 Topic
```

### 3. 渐进式增强

- **Phase 1**：纯 HAL + HTTP API
- **Phase 2**：+ WebSocket 遥测
- **Phase 3**：+ MQTT 集成（可选）
- **Phase 4**：+ ROS 2 桥接（如需要）

---

## 最终决策记录

| 日期 | 决策 | 依据 |
|------|------|------|
| 2026-08 | 继续自研 HAL，不引入 ROS 2 | ROS 2 armhf 无预编译包，256MB RAM 不足 |
| 待定 | 评估 micro-ROS Client | 如后续需要对接 ROS 2 生态 |

---

## 参考资源

- rosbridge_suite：https://github.com/RobotWebTools/rosbridge_suite
- MQTT for IoT：https://mqtt.org/
- MRPT：https://www.mrpt.org/
- RobotWebTools：https://robotwebtools.github.io/
