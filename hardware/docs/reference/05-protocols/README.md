# 1.5 通信协议分析

> SDJQR02RR 中各传感器和执行器通过 I²C、SPI、UART 与主控通信。本节记录已知协议细节。

---

## 总线架构

```
                    ┌──────────────────┐
                    │  Allwinner A33    │
                    │  (主 SoC)         │
                    └──┬───┬───┬───┬──┘
                       │   │   │   │
          ┌────────────┼───┼───┼───┼────────────┐
          │ I²C0       │I²C│SPI│UART│            │
          │            │1  │0  │    │            │
     ┌────▼───┐  ┌────▼───┴───▼──┐ │   ┌───────▼──────┐
     │ MPU6050│  │  电源管理/    │ │   │ UART0: 调试  │
     │ (IMU)  │  │  AXP PMIC     │ │   │ UART1: STM32 │
     └────────┘  └───────────────┘ │   │ UART2: LDS   │
                                   │   └──────────────┘
```

---

## UART 协议分析

### UART1：主 SoC ↔ STM32 电机 MCU

**推测波特率**：115200 或 921600 bps

**推测帧格式**：
```
┌───────┬──────┬──────┬──────────┬──────┐
│ HEAD  │ CMD  │ LEN  │ PAYLOAD  │ CRC  │
│ 0xAA  │ 1B   │ 1B   │ 0-255B   │ 2B   │
└───────┴──────┴──────┴──────────┴──────┘
```

**推测指令集**（需逻辑分析仪验证）：

| 命令 | 功能 | Payload |
|------|------|---------|
| 0x01 | 设置左轮 PWM | [speed_h, speed_l, dir] |
| 0x02 | 设置右轮 PWM | [speed_h, speed_l, dir] |
| 0x03 | 设置主刷 | [speed_h, speed_l] |
| 0x04 | 设置边刷 | [speed_h, speed_l] |
| 0x05 | 设置风机 | [speed_h, speed_l] |
| 0x10 | 读取电机电流 | — |
| 0x11 | 读取编码器 | — |
| 0xFF | 紧急停止 | — |

### UART2：主 SoC ↔ LDS 激光雷达

**推测参数**：
- 波特率：230400 bps
- 数据位：8，停止位：1，无校验

**数据格式（类似 SLAMTEC 协议）**：
```
┌──────┬──────────────┬─────────────┬──────────┬──────┐
│ 0xA5 │  质量/标志   │ 角度(deg)   │ 距离(mm) │ CRC  │
│ 1B   │  1B          │ 2B (LE)     │ 2B (LE)  │ 1B   │
└──────┴──────────────┴─────────────┴──────────┴──────┘
```

---

## I²C 协议分析

### I²C0：MPU-6050 IMU

| 属性 | 值 |
|------|-----|
| 地址 | 0x68（AD0=GND）/ 0x69（AD0=VCC） |
| 速率 | 400kHz（Fast Mode） |
| 数据 | 3 轴加速度 + 3 轴陀螺仪，各 16-bit |

### I²C1：电源管理 / 电池电量计

可能连接的设备：
- **AXP223 PMIC**（地址 0x34）：电池电压、充电状态、电源轨控制
- **BQ27541 电量计**（地址 0x55）：精确电量、充放电循环

---

## SPI 协议分析

### SPI0：NOR Flash（推测）

部分 Allwinner 设备使用 SPI NOR Flash 存储 bootloader：

| 属性 | 值 |
|------|-----|
| 容量 | 16MB 或 32MB |
| 速度 | 50MHz |
| 内容 | SPL (First stage bootloader) |

---

## 逻辑分析仪验证方案

1. **工具**：Saleae Logic 8/16 或兼容设备
2. **信号**：同时抓取 UART TX/RX、I²C SDA/SCL
3. **触发**：电机运转时抓取 STM32 通信帧
4. **解码**：使用 PulseView / Sigrok 软件

---

## 参考资源

- SLAMTEC RPLIDAR 协议文档：https://www.slamtec.com/en/Support#rplidar-a-series
- MPU-6050 寄存器手册：https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
- Saleae Logic 分析仪：https://www.saleae.com/
- Sigrok/PulseView 开源逻辑分析：https://sigrok.org/
