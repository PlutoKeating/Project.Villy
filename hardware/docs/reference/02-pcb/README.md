# 1.2 PCB 布局与元器件

> 基于网络上的拆机报告（Laptopmain、YouTube、4PDA 论坛）整理的主板结构分析。

---

## 主板整体结构

SDJQR01RR 内部主要有两块 PCB：

### 主板（Mainboard）

位于机器内部中央，承载：
- Allwinner R16 SoC + DDR3 RAM + NAND Flash
- WiFi 模块（RTL8189ETV，板载或子板）
- IMU 传感器（MPU-6050）
- 电源管理电路
- 音频放大器
- 对外连接器（LDS、电机驱动板、传感器板）

### 电机驱动板（Motor Driver Board）

位于底盘，承载：
- STM32F103 MCU（电机控制）
- 驱动轮 MOSFET H 桥驱动
- 主刷/边刷/风机 MOSFET 驱动
- 过流检测电路
- 与主板通过排线（UART + GPIO）连接

---

## 关键连接器

| 连接器 | 功能 | 引脚数 | 说明 |
|--------|------|--------|------|
| J1 | LDS 激光雷达 | 4-6 pin | UART + 供电（5V） |
| J2 | 电机驱动板 | 8-10 pin | UART + GPIO |
| J3 | 电池 | 4 pin | Vbat + GND + NTC + 通信 |
| J4 | 充电座 | 2 pin | 充电输入 |
| J5 | WiFi 天线 | U.FL/IPEX | 板载天线或外接 |
| J6 | 扬声器 | 2 pin | 音频输出 |
| J7 | 前碰撞传感器 | 2-4 pin | 微动开关 |
| J8 | 悬崖传感器×4 | 8-12 pin | IR LED + 光电管 |

---

## 元器件布局参考

> 以下为基于社区公开拆机照片的推断，实际需拆机确认。

### 主板 TOP 面

- 中央：Allwinner R16（BGA，有散热片覆盖）
- 左侧：DDR3 RAM（BGA，与 R16 相邻）
- 右侧：NAND Flash（TSOP-48 或 BGA）
- 角落：RTL8189ETV WiFi 模块
- 边缘：UART 测试点（4 个焊盘）

### 主板 BOTTOM 面

- 电源管理 IC（AXP 系列，推测 AXP223）
- MPU-6050 IMU
- 音频 Codec + 功放
- microUSB 或测试接口

---

## 参考资源

- Laptopmain 拆解：https://www.laptopmain.com/xiaomi-mi-robot-vacuum-teardown/
- YouTube 拆机视频：https://www.youtube.com/watch?v=wglJz23Gt4w
- AliExpress 替换主板照片：https://www.aliexpress.com/item/33021182316.html
- Dustcloud 文档仓库 PCB 照片：https://github.com/dgiese/dustcloud-documentation
