# 1.1 SoC 与关键芯片识别

> CRL200S 主板采用 Allwinner A33 + GigaDevice GD32F103VCT6 双处理器架构。

---

## 双处理器架构

```
┌─────────────────────────────────────────────────────┐
│                  CRL200S 主板                         │
│                                                     │
│  ┌──────────────────┐    ┌──────────────────────┐   │
│  │ Allwinner A33     │    │ GD32F103VCT6          │   │
│  │ (应用处理器)       │◄──►│ (实时电机控制 MCU)      │   │
│  │                   │UART│                       │   │
│  │ • Linux 系统       │ 3  │ • 驱动轮 BLDC 控制     │   │
│  │ • WiFi / 云通信    │    │ • 主刷/边刷/风机 PWM   │   │
│  │ • SLAM 导航        │    │ • 传感器采集与预处理    │   │
│  │ • 用户交互          │    │ • 过流保护             │   │
│  └──────────────────┘    └──────────────────────┘   │
│           │                          │              │
│           │ I2C/SPI/UART             │ GPIO/PWM     │
│           ▼                          ▼              │
│    传感器 + 激光雷达            电机 + 编码器         │
└─────────────────────────────────────────────────────┘
```

> 来源：codetiger/VacuumRobot — 已通过逻辑分析仪验证的连接关系

---

## Allwinner A33 深度分析

### 基本规格

| 属性 | 值 |
|------|-----|
| **架构** | ARM Cortex-A7 (ARMv7-A) |
| **核心数** | 4 核 |
| **主频** | 最高 1.2 GHz |
| **制程** | 40nm |
| **GPU** | Mali400MP2 |
| **RAM 支持** | DDR3 / DDR3L / LPDDR3 |
| **封装** | BGA-282 (14mm × 14mm) |
| **功耗** | 极低功耗设计，支持 DVFS |

### 与 R16 的关系

A33 与 R16 是 **pin-to-pin 兼容** 的芯片。在主线 Linux 中，两者都使用 `sun8i-a33` 平台代码。差异极小：

| 差异点 | A33 | R16 |
|--------|-----|-----|
| 目标市场 | 平板/通用 | 物联网专用 |
| 功耗优化 | 标准 | 增强 (DVFS) |
| 内核兼容 | sun8i-a33 | sun8i-a33 (相同) |

### 主线 Linux 支持状态

| 功能 | 支持状态 | 说明 |
|------|---------|------|
| SMP（4 核） | ✅ 主线 | 稳定 |
| GPIO | ✅ 主线 | pinctrl 驱动 |
| UART | ✅ 主线 | 6 路，8250 兼容 |
| I²C | ✅ 主线 | 4 路 TWI，mv64xxx |
| SPI | ✅ 主线 | sun6i-spi |
| MMC/SDIO | ✅ 主线 | sunxi-mmc |
| USB OTG | ✅ 主线 | **micro USB 口使用此接口** |
| PWM | ✅ 主线 | sunxi-pwm |
| Mali GPU | ⚠️ Lima 驱动 | 开源，实验性 |

---

## 电机控制 MCU — GD32F103VCT6

| 属性 | 值 |
|------|-----|
| **制造商** | GigaDevice（兆易创新） |
| **内核** | ARM Cortex-M3 @ 108MHz |
| **Flash** | 256 KB |
| **RAM** | 48 KB |
| **封装** | LQFP-100 |
| **与 A33 通信** | **UART3**，115200 bps，8N1，无流控，自定义二进制协议 |

> ⚠️ 注意：不是 STM32F103！虽然 GD32 与 STM32 部分兼容，但寄存器细节有差异。

### A33 ↔ GD32 通信协议（已验证）

```
┌────────┬──────┬──────┬──────────────┬──────┐
│ HEAD   │ CMD  │ LEN  │ PAYLOAD      │ CRC  │
│ 0x55   │ 1B   │ 1B   │ 0-255B       │ 1B   │
└────────┴──────┴──────┴──────────────┴──────┘
```

> 来源：codetiger/VacuumRobot/Research/GD32F1/README.md — 通过逻辑分析仪完全逆向

---

## 关键外设芯片

### WiFi 模块 — RTL8189ETV

| 属性 | 值 |
|------|-----|
| **芯片** | Realtek RTL8189ETV |
| **接口** | SDIO 2.0 |
| **协议** | 802.11 b/g/n, 2.4 GHz |
| **驱动** | rtl8189es（主线 staging） |

### IMU — MPU-6050

| 属性 | 值 |
|------|-----|
| **类型** | 6 轴（加速度计 + 陀螺仪） |
| **接口** | I²C0，地址 0x68 |
| **驱动** | `inv-mpu6050`（主线） |

### PMIC — AXP223

| 属性 | 值 |
|------|-----|
| **功能** | 21 通道电源管理 |
| **接口** | I²C1 |
| **职责** | 电池充电、电源轨控制、电压监测 |

> 来源：codetiger/VacuumRobot/Research/Motherboard/Connection_Evidence.md

---

## Micro USB 接口

CRL200S 主板上有一个 **Micro USB 母座**（可能位于背面或电池仓），直连 A33 的 USB OTG 控制器：

- ✅ **ADB Shell**：Android Debug Bridge，免焊接获得 root 权限
- ✅ **FEL 模式**：Allwinner BootROM USB 刷写，无需短接 NAND
- ✅ **不需要任何焊接**：直接用 Micro USB 数据线连接 PC

> 详见 [1.4 调试接口](../04-debug/README.md)

---

## 社区确认的芯片清单

| 芯片 | 功能 | 封装 | 来源 |
|------|------|------|------|
| Allwinner A33 | 主 SoC | BGA-282 | codetiger 验证 |
| GD32F103VCT6 | 电机控制 MCU | LQFP-100 | codetiger 验证 |
| RTL8189ETV | WiFi | QFN | 拆机确认 |
| MPU-6050 | 6 轴 IMU | QFN-24 | I²C 扫描确认 |
| AXP223 | PMIC | QFN | codetiger 验证 |
| NAND Flash | 存储 | TSOP/BGA | 512MB |

---

## 参考资源

- codetiger/VacuumRobot — 完整硬件逆向：https://github.com/codetiger/VacuumRobot
- codetiger/VacuumTiger — CRL200S 开源固件：https://github.com/codetiger/VacuumTiger
- A33 数据手册：https://linux-sunxi.org/A33
- GD32F103 数据手册：https://www.gigadevice.com/product/mcu/gd32f103
- AXP223 数据手册：http://dl.linux-sunxi.org/AXP/AXP223-en.pdf

---

*上一节：[第 1 章：硬件逆向工程参考](../README.md)*  
*下一节：[1.2 PCB 布局与元器件](../02-pcb/README.md)*
