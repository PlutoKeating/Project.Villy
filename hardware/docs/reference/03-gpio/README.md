# 1.3 GPIO 引脚映射

> 本节记录 Allwinner R16 SoC GPIO 引脚与外设的连接关系。最终映射需拆机后通过万用表通断测试和内核 `sysfs` 验证。

---

## Allwinner R16 GPIO 组概览

| GPIO 组 | 引脚数 | 推测用途 |
|---------|--------|----------|
| PA | 22 | UART、JTAG |
| PB | 16 | SDIO (WiFi)、MMC |
| PC | 25 | SPI、NAND |
| PD | 17 | LCD（未用） |
| PE | 16 | I²C、PWM |
| PF | 7  | SD Card Detect |
| PG | 13 | UART、I²C |
| PH | 27 | GPIO、IRQ |
| PL | 12 | 电源、复位 |
| PM | 8  | （保留） |

---

## 功能引脚映射（待验证）

### UART 接口

| UART | TX | RX | 连接外设 |
|------|-----|-----|----------|
| UART0 | PA4 | PA5 | **调试串口**（3.3V TTL） |
| UART1 | PG6 | PG7 | STM32 电机控制 MCU |
| UART2 | PB0 | PB1 | LDS 激光雷达 |
| UART3 | PH4 | PH5 | 超声波传感器（可能） |

### I²C 总线

| 总线 | SDA | SCL | 连接外设 |
|------|-----|-----|----------|
| I²C0 | PA11 | PA12 | MPU-6050 IMU |
| I²C1 | PE13 | PE12 | 电源管理 / 电池电量计 |
| I²C2 | PB4 | PB5 | 保留 |

### SPI 总线

| 总线 | CS | CLK | MOSI | MISO | 连接外设 |
|------|-----|-----|------|------|----------|
| SPI0 | PC0 | PC2 | PC1 | PC3 | NOR Flash（可能） |

### SDIO（WiFi）

| 信号 | 引脚 | 说明 |
|------|------|------|
| SDIO CLK | PB15 | 时钟 |
| SDIO CMD | PB14 | 命令 |
| SDIO D0-D3 | PB8-PB11 | 数据线 |

### PWM（电机控制）

| PWM 通道 | 引脚 | 用途 |
|----------|------|------|
| PWM0 | PE12 | 左驱动轮 |
| PWM1 | PE13 | 右驱动轮 |
| PWM2 | PH10 | 主刷 |
| PWM3 | PH11 | 边刷/风机 |

---

## 验证方法

1. **拆机 + 万用表通断测试**：从 SoC 焊盘追踪到连接器
2. **原厂固件设备树提取**：通过 FEL 模式 dump NAND，反编译 DTB
3. **主线内核 GPIO sysfs 探测**：
   ```bash
   echo PA0 > /sys/class/gpio/export
   cat /sys/class/gpio/gpio0/direction
   ```

---

## 参考资料

- linux-sunxi GPIO 文档：https://linux-sunxi.org/GPIO
- Allwinner R16 Datasheet Pinmux 章节
- sunxi-pinctrl 绑定文档（内核 Documentation/devicetree/bindings/pinctrl/）
