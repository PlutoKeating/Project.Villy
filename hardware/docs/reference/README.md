# 第 1 章：硬件逆向工程参考

> 本章基于网络调研和社区资源，系统梳理 SDJQR01RR 硬件架构、关键芯片、通信协议和外设接口。

---

## 1.1 硬件概览

### 设备身份

| 属性 | 值 |
|------|-----|
| **产品名称** | 米家扫地机器人 / Mi Robot Vacuum |
| **型号** | SDJQR01RR（国行）/ STYTJ01YM |
| **代工厂** | 石头科技（Roborock） |
| **发布时间** | 2016 年 8 月 |
| **定位** | 初代激光导航扫地机器人 |

### 核心硬件参数

| 组件 | 规格 |
|------|------|
| **SoC** | Allwinner R16 (Quad Cortex-A7 @ 1.2GHz) |
| **GPU** | Mali400MP2 |
| **RAM** | 256 MB DDR3 |
| **存储** | 512 MB NAND Flash |
| **WiFi** | Realtek RTL8189ETV (2.4GHz b/g/n) |
| **激光雷达** | SLAMTEC RPLIDAR 或三方定制 LDS |
| **IMU** | InvenSense MPU-6050 / 类似 6 轴 |
| **超声波** | 前方超声波距离传感器 |
| **悬崖传感器** | 4 组红外对射（底部） |
| **电机** | 驱动轮×2（有刷/无刷）、主刷×1、边刷×1、风机×1 |
| **电池** | 14.4V / 5200mAh 锂电（4S） |

---

## 1.2 子章节导航

| 编号 | 文档 | 内容 |
|------|------|------|
| 1.1 | [SoC 与关键芯片识别](./01-soc/README.md) | Allwinner R16 深度分析、PCB 芯片清单 |
| 1.2 | [PCB 布局与元器件](./02-pcb/README.md) | 主板结构、元器件布局、连接器定义 |
| 1.3 | [GPIO 引脚映射](./03-gpio/README.md) | SoC 引脚→外设对照表 |
| 1.4 | [调试接口](./04-debug/README.md) | UART/JTAG/USB/FEL 接口位置与接线 |
| 1.5 | [通信协议分析](./05-protocols/README.md) | I²C、SPI、UART 总线上的传感器协议 |
| 1.6 | [传感器系统](./06-sensors/README.md) | LDS 激光雷达、IMU、超声、悬崖传感器 |
| 1.7 | [电机驱动系统](./07-motors/README.md) | 驱动轮、主刷、边刷、风机控制 |
| 1.8 | [电源管理](./08-power/README.md) | 电池、充电管理、电源树 |
| 1.9 | [WiFi 与通信模块](./09-connectivity/README.md) | RTL8189ETV、天线设计 |

---

## 1.3 快速参考：已知芯片清单

| 芯片 | 功能 | 封装 | 备注 |
|------|------|------|------|
| Allwinner R16 | 主 SoC | BGA-282 | Quad A7, Mali400MP2 |
| RTL8189ETV | WiFi | QFN | 2.4GHz, SDIO |
| MPU-6050 | 6 轴 IMU | QFN-24 | 加速度计+陀螺仪 |
| STM32F1xx | 电机控制 MCU | LQFP | PWM 驱动 |
| NAND Flash | 存储 | TSOP/BGA | 512MB, 来自 Micron/Toshiba |
| DDR3 | RAM | BGA | 256MB, 来自 Samsung/Hynix |

> **注：** 部分芯片型号需拆机后通过丝印确认。上表为基于社区拆机报告和 AliExpress 替换配件信息的推断。

---

## 1.4 关键社区资源

| 资源 | 链接 | 说明 |
|------|------|------|
| linux-sunxi R16 页面 | https://linux-sunxi.org/R16 | SoC 文档、内核支持状态 |
| R16 数据手册 | https://linux-sunxi.org/images/b/b3/R16_Datasheet_V1.4_(1).pdf | 官方 datasheet |
| Dustcloud 文档 | https://github.com/dgiese/dustcloud | 小米硬件逆向 |
| 4PDA 论坛 | https://4pda.to/forum/index.php?showtopic=881982 | 俄语社区，大量拆机/刷机讨论 |
| Roboter-Forum | https://www.roboter-forum.com/ | 德语社区，扫地机 root 讨论 |
| Laptopmain 拆解 | https://www.laptopmain.com/xiaomi-mi-robot-vacuum-teardown/ | 初代机拆解图文 |
| Hackaday 逆向 | https://hackaday.com/2019/10/24/reverse-engineering-xiaomi-iot-firmware/ | 小米 IoT 固件逆向方法 |

---

*下一节：[1.1 SoC 与关键芯片识别](./01-soc/README.md)*
