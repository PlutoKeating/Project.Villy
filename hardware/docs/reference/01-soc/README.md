# 1.1 SoC 与关键芯片识别

> Allwinner R16 为核心，辅以电机控制 MCU、WiFi 模块、传感器接口芯片。

---

## Allwinner R16 深度分析

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

### 接口资源

| 接口 | 数量 | 用途 |
|------|------|------|
| GPIO | 8 组（PA/PC/PD/PE/PF/PG/PH/PL） | 通用 I/O |
| UART | 6 路 | 调试串口、传感器通信 |
| TWI (I²C) | 4 路 | IMU、电源管理 |
| SPI | 2 路 | NOR Flash、传感器 |
| MIPI DSI | 4-lane | 显示屏（本设备未用） |
| LVDS | 1 路 | LCD（本设备未用） |
| USB OTG/HOST | 2 路 | FEL 刷写、调试 |
| SDIO | 3 路 | WiFi、SD 卡、eMMC |
| PWM | 4 路 | 电机调速 |
| ADC | 多路 | 电池电压检测、悬崖传感器 |
| Audio Codec | 内置 | 语音播报 |

### R16 与 A33 的关系

R16 与 Allwinner A33 是 Pin-to-Pin 兼容的芯片，共享相同的内核主线支持代码（`sun8i-a33`）。在主线 Linux 中，R16 使用 `sun8i-a33` 的设备树兼容字符串。这意味着：

- 可以直接复用 A33 的主线内核和设备树
- sunxi 社区对 A33 的支持已相当成熟
- 大多数外设驱动无需额外开发

### 主线 Linux 支持状态

| 功能 | 支持状态 | 说明 |
|------|---------|------|
| SMP（4 核） | ✅ 主线 | 稳定 |
| GPIO | ✅ 主线 | pinctrl 驱动 |
| UART | ✅ 主线 | 8250 兼容 |
| I²C | ✅ 主线 | mv64xxx 兼容 |
| SPI | ✅ 主线 | sun6i-spi |
| MMC/SDIO | ✅ 主线 | sunxi-mmc |
| USB OTG | ✅ 主线 | musb |
| PWM | ✅ 主线 | sunxi-pwm |
| Mali GPU | ⚠️ 部分 | Lima 驱动（实验性） |
| Video Decode | ⚠️ 部分 | cedrus（实验性） |
| Audio | ✅ 主线 | sun4i-codec |

---

## 关键外设芯片

### 电机控制 MCU — STM32F1xx（推测）

基于社区拆机报告和同类产品分析，扫地机通常使用一颗 STM32F103 系列 MCU 负责：

- 驱动轮 BLDC 电机 PWM 控制
- 主刷/边刷/风机电机驱动
- 过流保护与电流检测
- 与主 SoC 通过 UART 通信

**典型通信协议**：主 SoC (R16) ↔ STM32 通过 UART 发送指令帧，格式类似：

```
[HEADER][CMD][LEN][PAYLOAD][CRC]
```

### WiFi 模块 — RTL8189ETV

| 属性 | 值 |
|------|-----|
| **芯片** | Realtek RTL8189ETV |
| **接口** | SDIO 2.0 |
| **协议** | 802.11 b/g/n |
| **频段** | 2.4 GHz |
| **驱动** | rtl8189es（主线 staging） |

主线内核中 RTL8189ETV 的支持状态有限。可能需要使用厂商提供的 out-of-tree 驱动或从原厂固件中提取内核模块。

### IMU — MPU-6050 / ICM-20608

| 属性 | 值 |
|------|-----|
| **类型** | 6 轴（加速度计 + 陀螺仪） |
| **接口** | I²C（地址 0x68 或 0x69） |
| **驱动** | `inv-mpu6050`（主线） |

### NAND Flash

| 属性 | 推测值 |
|------|--------|
| **容量** | 512MB (4Gbit) |
| **类型** | SLC/MLC NAND |
| **接口** | 8-bit 并行 NAND |
| **分区** | 包含 bootloader、kernel、rootfs、app、data 等 |

---

## 社区芯片识别参考

以下资源可辅助芯片识别：

- **Dustcloud 文档仓库**：https://github.com/dgiese/dustcloud-documentation — 包含大量小米设备的 PCB 照片和数据手册
- **R16 官方数据手册**：https://linux-sunxi.org/images/b/b3/R16_Datasheet_V1.4_(1).pdf
- **Allwinner 官方**：https://www.allwinnertech.com/uploads/pdf/202102041951349c.pdf

---

*上一节：[第 1 章：硬件逆向工程参考](../README.md)*  
*下一节：[1.2 PCB 布局与元器件](../02-pcb/README.md)*
