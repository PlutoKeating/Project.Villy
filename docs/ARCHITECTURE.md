# 项目架构 · Architecture

> 本文档描述 Project.Villy 的系统架构、模块边界、技术选型依据和接口契约。

---

## 目标硬件

| 组件 | 型号 |
|------|------|
| **主板** | CRL200S_01_V006 (3irobotix / Dreame) |
| **SoC** | Allwinner A33 (Quad Cortex-A7 @ 1.2GHz) |
| **电机 MCU** | GD32F103VCT6 (Cortex-M3 @ 108MHz) |
| **PMIC** | AXP223 |
| **RAM** | 256 MB DDR3 |
| **存储** | 512 MB NAND Flash |
| **调试接口** | Micro USB OTG → ADB + FEL（免焊接） |

## 总体架构

```
┌─────────────────────────────────────────────────────┐
│                    操作者 / 开发者                     │
│         Browser Dashboard  │  CLI / SSH / ADB        │
└──────────────┬──────────────┴───────────┬────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌───────────────────────┐
│       frontend/          │  │   backend/             │
│  React + Tailwind CSS    │  │   Flask 3.x + Python   │
│  Port 5173 (dev)         │  │   3.11+                │
│                          │  │   Port 5000            │
│  • 实时仪表盘             │  │                        │
│  • 遥控面板               │  │   • REST API           │
│  • 传感器可视化            │  │   • HMAC 认证          │
└──────────┬───────────────┘  │   • HAL 抽象层         │
           │                  │   • WebSocket 遥测     │
           │                  └───────────┬───────────┘
           │  HTTP / WS (HMAC-SHA256)     │
           └──────────────┬───────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                   HAL (硬件抽象层)                     │
│  backend/app/hal/                                    │
│                                                     │
│  • 统一传感器接口 (SensorInterface)                    │
│  • 统一电机接口 (MotorInterface)                       │
│  • GPIO 管理 (GpioController)                        │
│  • 激光雷达驱动适配 (LidarDriver)                       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│               Linux Kernel (sun8i-a33) + 设备驱动      │
│  firmware/                                           │
│                                                     │
│  • 定制 Linux 内核 (主线 sunxi)                        │
│  • 设备树 (DTS: sun8i-a33-crl200s.dts)               │
│  • GPIO / I2C / SPI / UART / PWM 驱动               │
│  • USB OTG (ADB + FEL)                              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          硬件层 — CRL200S (Allwinner A33 + GD32)       │
│  hardware/                                           │
│                                                     │
│  ┌──────────────┐    UART3     ┌──────────────────┐  │
│  │ Allwinner A33 │◄──────────►│ GD32F103VCT6      │  │
│  │ (应用处理器)   │  115200 8N1 │ (电机控制 MCU)    │  │
│  └──────┬───────┘              └────────┬─────────┘  │
│         │ I2C/SPI/UART/USB              │ GPIO/PWM   │
│         ▼                               ▼            │
│  • LDS 激光雷达      • MPU-6050 IMU                  │
│  • 超声波传感器       • 悬崖传感器                     │
│  • RTL8189ETV WiFi   • 驱动轮×2 / 主刷 / 边刷 / 风机  │
│  • Micro USB (ADB+FEL)                              │
└─────────────────────────────────────────────────────┘
```

---

## 模块边界与接口

### `hardware/` → `firmware/`

| 接口 | 说明 |
|------|------|
| GPIO 映射表 | 完整引脚功能定义 |
| 通信协议文档 | I2C/SPI/UART 总线上的传感器协议 |
| 芯片数据手册 | A33、GD32、AXP223 的寄存器级文档 |

### `firmware/` → `backend/`

| 接口 | 说明 |
|------|------|
| `/sys/class/gpio/` | GPIO sysfs 接口 |
| `/dev/i2c-*` | I2C 设备节点 |
| `/dev/ttyS*` | UART 设备节点（含 A33↔GD32 的 UART3） |
| `/sys/class/pwm/` | PWM 控制接口 |
| 内核模块 | `.ko` 驱动模块 |

### `backend/` → `frontend/`

| 接口 | 说明 |
|------|------|
| `GET /api/v1/status` | 机器人状态摘要 |
| `GET /api/v1/sensors` | 传感器实时数据 |
| `POST /api/v1/motors` | 电机控制指令 |
| `WS /api/v1/ws/telemetry` | WebSocket 遥测流 |

---

## 技术选型

### 后端: Python 3.11+ / Flask

| 考量维度 | 决策 |
|----------|------|
| **硬件资源** | A33 仅 256MB RAM，Flask 比 Django/FastAPI 更轻量 |
| **生态兼容** | Python 在 ARMv7 有完整支持 |
| **HAL 开发** | Python 直接操作 sysfs/gpio/I2C |

### 调试: Micro USB ADB + FEL

| 考量维度 | 决策 |
|----------|------|
| **免焊接** | CRL200S 原生 Micro USB 口直连 A33 USB OTG |
| **ADB** | 获得 root shell，文件传输 |
| **FEL** | NAND 读写，直接刷写 |

---

*最后更新: 2026-08-09*
