# 1.4 调试接口

> CRL200S 主板提供**无需焊接**的 Micro USB 调试接口，以及备用的 UART 焊盘。

---

## 一、Micro USB — 免焊全功能调试口 ⭐

### 这是你的主调试接口

CRL200S 主板背面（或电池仓内）有一个 **Micro USB 母座**，直连 Allwinner A33 的 **USB OTG** 控制器。这意味着：

- **无需焊接任何东西**
- **无需拆机**（部分机型电池仓内有第二个 Micro USB）
- 一根 Micro USB 数据线即可完成所有操作

### 支持的两种模式

| 模式 | 用途 | 波特率 | 如何进入 |
|------|------|--------|----------|
| **ADB** | Root shell, 文件传输, 应用管理 | — | 正常开机后插 USB |
| **FEL** | NAND 读写, 内核加载, 固件刷写 | — | U-Boot 中 `fel` 命令或短接 NAND 引脚 |

### ADB 连接步骤

```bash
# 1. 用 Micro USB 数据线（必须是数据线！）连接机器人和 PC

# 2. 启动机器人，等待完全开机（约 30-60 秒）

# 3. PC 端检查设备
adb devices
# 输出示例：
# List of devices attached
# 0123456789ABCDEF    device

# 4. 获得 root shell！
adb shell
# 直接进入 root 权限的 shell
```

### 如果 ADB 不识别

部分 CRL200S 机型在启动后会快速关闭 ADB。使用 Valetudo 官方工具：

```bash
# 克隆工具
git clone https://github.com/Hypfer/valetudo-crl200s-root.git
cd valetudo-crl200s-root

# 运行 ADB 启用脚本（按提示操作）
chmod +x enable-adb.sh
./enable-adb.sh
```

脚本会在开机瞬间捕获 ADB 窗口并启用持久访问。

### FEL 模式

```bash
# 方法一：从 U-Boot 进入（如果 ADB shell 可用）
adb shell "reboot bootloader"  # 或
# 在 U-Boot 倒计时时按任意键 → 输入 fel

# 方法二：NAND 短接法（物理触发）
# 启动时短接 NAND 数据线中 D0-D7 任意两根 → BootROM 回退到 FEL

# 检测 FEL 设备
sudo sunxi-fel version
# AWUSBFEX soc=1667(A33) ver=0001 ...

# FEL 模式下的 Micro USB 口 = A33 USB OTG = 全功能刷写
```

---

## 二、UART 调试串口（备用）

### 接口特征

| 属性 | 值 |
|------|-----|
| 位置 | 主板边缘，4 个圆形焊盘 |
| 丝印 | 可能标记为 TX/RX/GND/VCC |
| 电平 | 3.3V TTL |
| 波特率 | **115200** bps, 8N1, 无流控 |

### 接线方法

```
USB-UART 模块 (3.3V!)        主板焊盘
   GND    ─────────────────  GND
   RX     ─────────────────  TX
   TX     ─────────────────  RX
   VCC    ── 不接（绝不要接5V！）
```

> ⚠️ CRL200S 是 3.3V 系统！使用 5V USB-UART 会烧坏 SoC！

### 焊接永久引出方案（如果 Micro USB 不可用）

```
方案 A：杜邦线直焊
  焊盘 → 杜邦线 → 外壳开孔引出 4-pin JST 连接器

方案 B：内置 USB-UART 模块
  焊盘 → CP2102 模块 → Micro USB 母座固定在外壳上
  效果：跟原生 Micro USB 一样方便
```

---

## 三、调试优先级总结

| 优先级 | 接口 | 需要焊接？ | 可获得什么 |
|--------|------|-----------|-----------|
| 🥇 | **Micro USB (ADB)** | ❌ 不需要 | Root shell, 文件传输 |
| 🥈 | **Micro USB (FEL)** | ❌ 不需要 | NAND 读写, 内核加载 |
| 🥉 | UART 焊盘 | ⚠️ 需要焊接 | U-Boot 控制台, 内核日志 |

**结论：对于 CRL200S，Micro USB 口就是你需要的全部调试接口。不需要焊接。**

---

## 参考资源

- Hypfer/valetudo-crl200s-root：https://github.com/Hypfer/valetudo-crl200s-root
- codetiger/VacuumRobot/Connection_Evidence：https://github.com/codetiger/VacuumRobot/blob/main/Research/Motherboard/Connection_Evidence.md
- Makers Pet Proscenic M6 Pro 教程（同款 CRL200S 板，ADB 实操）：https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/
- linux-sunxi FEL 文档：https://linux-sunxi.org/FEL
