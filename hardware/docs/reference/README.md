# 第 1 章：硬件逆向工程参考

> 本章基于社区逆向工程成果（codetiger/VacuumRobot），系统梳理 CRL200S (Allwinner A33 + GD32F103) 硬件架构。

---

## 1.1 硬件概览

### 设备身份

| 属性 | 值 |
|------|-----|
| **主板型号** | CRL200S_01_V006 (2018-11-30) |
| **制造商** | 3irobotix ( Dreame 供应链 ) |
| **对应机型** | 小米 Mijia 1S (SDJQR02RR)、Viomi V2/V7、Cecotec Conga、Proscenic M6 Pro 等 |
| **SoC** | Allwinner A33 (4×Cortex-A7) |
| **电机 MCU** | GigaDevice GD32F103VCT6 (Cortex-M3) |
| **PMIC** | AXP223 |

### 核心硬件参数

| 组件 | 规格 |
|------|------|
| **SoC** | Allwinner A33 (Quad Cortex-A7 @ 1.2GHz) |
| **GPU** | Mali400MP2 |
| **RAM** | 256 MB DDR3 |
| **存储** | 512 MB NAND Flash |
| **WiFi** | Realtek RTL8189ETV (2.4GHz b/g/n, SDIO) |
| **激光雷达** | LDS 激光测距传感器 (UART) |
| **IMU** | MPU-6050 (I²C0, 0x68) |
| **超声波** | 前方超声波距离传感器 |
| **悬崖传感器** | 4 组红外对射（底部） |
| **电机** | 驱动轮×2, 主刷×1, 边刷×1, 风机×1 |
| **电池** | 14.4V / 5200mAh 锂电 (4S) |

---

## 1.2 子章节导航

| 编号 | 文档 | 内容 |
|------|------|------|
| 1.1 | [SoC 与关键芯片识别](./01-soc/README.md) | A33 + GD32 双处理器架构 |
| 1.2 | [PCB 布局与元器件](./02-pcb/README.md) | CRL200S 主板结构与连接器 |
| 1.3 | [GPIO 引脚映射](./03-gpio/README.md) | A33 引脚→外设对照表 |
| 1.4 | [调试接口](./04-debug/README.md) | Micro USB ADB/FEL（免焊！）+ UART |
| 1.5 | [通信协议分析](./05-protocols/README.md) | A33↔GD32 UART3 协议, I²C, SPI |

---

## 1.3 已确认的芯片清单

| 芯片 | 功能 | 封装 | 验证来源 |
|------|------|------|---------|
| Allwinner A33 | 主 SoC | BGA-282 | codetiger 验证 |
| GD32F103VCT6 | 电机控制 MCU | LQFP-100 | codetiger 验证 |
| RTL8189ETV | WiFi | QFN | 拆机确认 |
| MPU-6050 | 6 轴 IMU | QFN-24 | I²C 扫描 |
| AXP223 | 电源管理 PMIC | QFN | codetiger 验证 |
| NAND Flash | 存储 | TSOP/BGA | 512MB |

---

## 1.4 关键社区资源（CRL200S 专用）

| 资源 | 链接 | 说明 |
|------|------|------|
| codetiger/VacuumRobot | https://github.com/codetiger/VacuumRobot | **完整逆向工程**：元器件图、连接验证、协议分析 |
| codetiger/VacuumTiger | https://github.com/codetiger/VacuumTiger | CRL200S 开源固件 (Rust) |
| Hypfer/valetudo-crl200s-root | https://github.com/Hypfer/valetudo-crl200s-root | ADB 一键 root 工具 |
| Makers Pet CRL200S→ROS2 | https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/ | 同款板子接 ROS 2 教程 |
| robotinfo.dev | https://robotinfo.dev/ | Dennis Giese 的机器人硬件数据库 |
| linux-sunxi A33 | https://linux-sunxi.org/A33 | SoC 主线支持文档 |

---

*下一节：[1.1 SoC 与关键芯片识别](./01-soc/README.md)*
