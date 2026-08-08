# 1.4 调试接口

> SDJQR01RR 提供了多种调试和刷写入口。本节记录所有已知的调试接口及其使用方法。

---

## 一、UART 调试串口

### 接口特征

| 属性 | 值 |
|------|-----|
| 位置 | 主板边缘，通常为 4 个焊盘或排针孔 |
| 电平 | 3.3V TTL |
| 波特率 | **115200** bps（常见），部分设备 1500000 |
| 引脚 | GND, TX, RX（VCC 不接） |

### 接线方法

```
USB-UART 模块          SDJQR01RR 主板
   GND    ────────────  GND
   RX     ────────────  TX
   TX     ────────────  RX
   (VCC   ── 不接 ──    VCC 引脚)
```

### 预期的启动日志内容

- **BROM**（Boot ROM）信息：Allwinner 芯片的上电第一条打印
- **SPL**（Secondary Program Loader）：U-Boot SPL
- **U-Boot**：引导加载器交互提示符（按任意键进入）
- **Kernel**：Linux 内核启动日志（dmesg）
- **Login**：可能直接进入 root shell 或需要密码

---

## 二、FEL 模式（USB 刷写）

### 原理

FEL（Failsafe Engine Loader）是 Allwinner BootROM 内置的 USB 恢复模式。当 SoC 无法从 NAND/SD 正常启动时，会自动进入 FEL 模式。

### 进入 FEL 模式的方法

1. **NAND 数据线短路法**（推荐）：
   - 在通电启动时，短接 NAND Flash 的 D0-D7 数据线中某两根
   - SoC 读取 NAND 失败 → 回退到 FEL 模式
   - **社区报告此方法在小米扫地机上有效**

2. **FEL 按钮法**（如果有）：
   - 按住特定按钮（如 Home 键）同时通电

3. **SD 卡 FEL 触发**：
   - 制作特殊 SD 卡，写入 FEL 触发镜像

### 连接方法

```
PC USB 口 ──USB 线── 机器人 microUSB/测试口
```

进入 FEL 后，PC 上运行：
```bash
# 检查是否检测到设备
sudo sunxi-fel version

# 输出示例：
# AWUSBFEX soc=1667(R16) ver=0001 ......
```

### FEL 可以做什么

| 操作 | 命令示例 |
|------|---------|
| 读取 SoC 信息 | `sunxi-fel version` |
| 读取内存 | `sunxi-fel read 0x40000000 0x1000 dump.bin` |
| 写入内存 | `sunxi-fel write 0x42000000 zImage` |
| 执行代码 | `sunxi-fel exec 0x42000000` |
| Dump NAND | `sunxi-fel spiflash-read 0 0x20000000 nand-dump.bin` |

---

## 三、microUSB 接口

主板可能有一个 microUSB 接口用于：
- FEL 模式刷写（通过 USB OTG 功能）
- 充电（部分型号）

需拆机确认是否存在及位置。

---

## 四、JTAG / SWD

Allwinner R16 支持 JTAG 调试，但：
- 需要专门的 JTAG 调试器（如 J-Link、OpenOCD 兼容）
- 引脚可能未引出，需要飞线焊接
- 社区中使用 JTAG 的案例较少，UART + FEL 已覆盖绝大多数需求

---

## 参考资源

- linux-sunxi FEL 文档：https://linux-sunxi.org/FEL
- sunxi-tools GitHub：https://github.com/linux-sunxi/sunxi-tools
- Hackaday FEL 逆向案例：https://hackaday.com/2019/10/24/reverse-engineering-xiaomi-iot-firmware/
- Dustbuilder FEL 使用指南：https://github.com/dgiese/dustbuilder-howto
