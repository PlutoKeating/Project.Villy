# Hardware 硬件逆向工程

> 本模块负责小米扫地机器人 SDJQR02RR 的硬件逆向分析。

## 工作范围

- PCB 拆解与芯片识别
- GPIO 引脚追踪与映射
- 通信协议分析（I²C、SPI、UART）
- 调试接口定位（UART / JTAG / USB）
- 原厂固件提取与分析
- 可刷入 Linux 发行版调研

## 快速入口

| 文档 | 内容 |
|------|------|
| [芯片识别记录](docs/chip-identification.md) | PCB 上所有关键芯片型号与功能 |
| [GPIO 映射](docs/gpio-map.md) | SoC 引脚 → 外设对应表 |
| [调试接口](docs/debug-ports.md) | UART/JTAG/USB 触点位置与接线 |
| [启动日志](docs/boot-log.md) | 串口抓取的 bootloader / kernel 日志 |
| [通信协议](docs/protocols.md) | I²C/SPI/UART 传感器通信协议分析 |
| [分区布局](docs/partition-layout.md) | NAND Flash 分区表 |
| [Linux 发行版列表](docs/linux-distros.md) | 可移植到此硬件的 Linux 发行版调研 |

## 实物照片

`teardown/` 目录存储 PCB 高清正反面照片。由于文件体积较大，照片不入 Git 仓库（已通过 `.gitignore` 排除）。

## 启动日志

Bootloader + Kernel 日志通过串口抓取后存入 `docs/boot-log.md`，包含完整十六进制 dump 和注释分析。

---

> 所有操作记录严格遵循 [AGENT.md](../../AGENT.md) 中定义的「发现→方案→结果→复盘」四要素规范。
