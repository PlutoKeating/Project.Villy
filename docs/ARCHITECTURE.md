# 项目架构 · Architecture

> 本文档描述 Project.Villy 的系统架构、模块边界、技术选型依据和接口契约。
> 所有跨模块决策均在此记录。

---

## 总体架构

```
┌─────────────────────────────────────────────────────┐
│                    操作者 / 开发者                     │
│         Browser Dashboard  │  CLI / SSH              │
└──────────────┬──────────────┴───────────┬────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌───────────────────────┐
│       frontend/          │  │   backend/             │
│  React + Tailwind CSS    │  │   Flask 3.x + Python   │
│  Port 5173 (dev) /       │  │   3.14+                │
│  served by Flask (prod)  │  │   Port 5000            │
│                          │  │                        │
│  • 实时仪表盘             │  │   • REST API           │
│  • 遥控面板               │  │   • HMAC 认证          │
│  • 传感器可视化            │  │   • HAL 抽象层         │
│  • 日志查看               │  │   • WebSocket 遥测     │
└──────────┬───────────────┘  └───────────┬───────────┘
           │                              │
           │  HTTP / WS (HMAC-SHA256)     │
           │                              │
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
│               Linux Kernel + 设备驱动                 │
│  firmware/                                           │
│                                                     │
│  • 定制 Linux 内核 (主线 / sunxi)                     │
│  • 设备树 (DTS)                                      │
│  • GPIO / I2C / SPI / UART 驱动                     │
│  • PWM 电机控制                                      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          硬件层 — Allwinner R16 (SDJQR01RR)           │
│  hardware/                                           │
│                                                     │
│  • LDS 激光雷达     • 超声波雷达                       │
│  • IMU             • 悬崖传感器                       │
│  • 驱动轮 ×2       • 主刷 / 边刷 / 风机                │
│  • WiFi (RTL8189)  • 电池管理                         │
└─────────────────────────────────────────────────────┘
```

---

## 模块边界与接口

### `hardware/` → `firmware/`

| 接口 | 说明 |
|------|------|
| GPIO 映射表 | 完整引脚功能定义 |
| 通信协议文档 | I2C/SPI/UART 总线上的传感器协议 |
| 芯片数据手册 | 关键芯片的寄存器级文档 |

### `firmware/` → `backend/`

| 接口 | 说明 |
|------|------|
| `/sys/class/gpio/` | GPIO sysfs 接口 |
| `/dev/i2c-*` | I2C 设备节点 |
| `/dev/ttyS*` | UART 设备节点 |
| `/sys/class/pwm/` | PWM 控制接口 |
| 内核模块 | `.ko` 驱动模块 |

### `backend/` → `frontend/`

| 接口 | 说明 |
|------|------|
| `GET /api/v1/status` | 机器人状态摘要 |
| `GET /api/v1/sensors` | 传感器实时数据 |
| `POST /api/v1/motors` | 电机控制指令 |
| `WS /api/v1/ws/telemetry` | WebSocket 遥测流 |
| `GET /api/v1/system/info` | 系统信息 |

所有 API 请求必须携带 HMAC-SHA256 签名头（详见 `backend/docs/auth-scheme.md`）。

---

## 技术选型

### 后端：Python 3.14+ / Flask

| 考量维度 | 决策 |
|----------|------|
| **硬件资源** | Allwinner R16 仅 256MB RAM，Flask 比 Django/FastAPI 更轻量 |
| **生态兼容** | Python 在 ARMv7 有完整支持，Flask 依赖链极短 |
| **HAL 开发** | Python 直接操作 sysfs/gpio/I2C，无需中间层 |
| **社区** | Flask 在嵌入式/IoT 领域有大量先例 |

### 前端：React + Tailwind CSS

| 考量维度 | 决策 |
|----------|------|
| **仪表盘需求** | React 生态有成熟的图表库（Recharts）和实时数据方案 |
| **响应式** | Tailwind 原生支持 mobile-first，适合手机遥控场景 |
| **构建产物** | Vite 输出纯静态文件，可直接由 Flask 托管 serve |

### 认证：HMAC-SHA256 签名

| 考量维度 | 决策 |
|----------|------|
| **硬件开销** | HMAC-SHA256 极轻量，远优于 JWT (RSA/ECDSA) |
| **安全性** | 防重放（timestamp + nonce）、防篡改（body hash） |
| **实现** | Python `hmac` 标准库，零外部依赖 |

### ROS 2 选型（待定）

| 考量维度 | 分析 |
|----------|------|
| **有利** | 标准化 SLAM / 导航栈、社区生态 |
| **不利** | 256MB RAM 可能不足、ARMv7 预编译包稀缺 |
| **决策** | 先自行实现轻量 HAL，后续评估 ROS 2 micro-ROS 可行性 |

---

## 数据流

```
传感器 → 内核驱动 → HAL (Python) → Flask API → WebSocket → React Dashboard
                                          │
                                          └──→ HTTP Response → CLI / Script
```

- **遥测流**（高频）：WebSocket 推送 IMU、里程计、激光雷达数据
- **指令流**（低频）：HTTP POST 电机/云台控制，HMAC 签名验证
- **日志流**：各模块 `docs/` 中的 Markdown 文档

---

## 安全边界

- 禁止匿名 API 访问（强制 HMAC 签名）
- 禁止机器人向外网暴露 API 端口
- 所有固件写入操作需显式本地授权
- 私有凭据、WiFi 密钥、设备唯一标识符不在仓库中存储

---

*最后更新：2026-08-08*
