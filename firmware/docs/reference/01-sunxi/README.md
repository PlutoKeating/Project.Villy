# 2.1 sunxi 生态与主线内核

> linux-sunxi 社区是 Allwinner SoC 主线 Linux 支持的核心驱动力。本节梳理 sunxi 生态的关键资源、支持状态和开发流程。

---

## linux-sunxi 社区概览

**网站**：https://linux-sunxi.org

linux-sunxi 是一个社区驱动的开源项目，致力于为 Allwinner（全志）SoC 提供主线 Linux 内核支持。社区维护了：

- **主线内核补丁**：将 Allwinner SoC 支持推入 Linux 主线
- **U-Boot**：Allwinner 设备的主线引导加载器
- **sunxi-tools**：FEL 模式和设备管理工具集
- **文档 Wiki**：https://linux-sunxi.org/
- **邮件列表**：linux-sunxi@googlegroups.com

### R16 在 sunxi 中的定位

R16 使用 `sun8i` 平台代码，与 A33 共享内核支持：

```
SoC 家族：
  sun4i (A10)
  sun5i (A13, A10s)
  sun6i (A31, A31s)
  sun7i (A20)
  sun8i (A23, A33, R16, H3, H2+)  ← R16 在这里
  sun9i (A80)
  sun50i (A64, H5, H6 — ARM64)
```

### 内核配置前缀

```bash
# 使用 sunxi 多平台内核
make ARCH=arm multi_v7_defconfig sunxi_defconfig

# 或在 multi_v7_defconfig 基础上调整
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```

---

## 关键仓库

### 内核

| 仓库 | 说明 |
|------|------|
| `torvalds/linux` | Linux 主线（推荐，已包含大部分 sunxi 代码） |
| `linux-sunxi/linux-sunxi` | sunxi 社区的开发分支（包含未主线化的补丁） |
| `kernel.googlesource.com/pub/scm/linux/kernel/git/sunxi/linux` | sunxi 内核镜像 |

**推荐策略**：使用主线内核（6.x）+ sunxi 社区补丁（仅当需要未主线化功能时）。

### U-Boot

| 仓库 | 说明 |
|------|------|
| `u-boot/u-boot` | 主线 U-Boot（推荐，包含 sunxi 支持） |

主线 U-Boot 已支持 Allwinner A33/A33，使用 `Sinovoip_BPI_M2_Plus` 或 `bananapi_m2_magic` 作为参考配置。

### sunxi-tools

```bash
git clone https://github.com/linux-sunxi/sunxi-tools.git
cd sunxi-tools
make
# 关键工具：
# - sunxi-fel: FEL 模式 USB 通信
# - sunxi-fexc: FEX 脚本编译器
# - sunxi-nand-part: NAND 分区工具
```

---

## 主线支持状态（A33）

| 功能 | 主线版本 | 状态 | 说明 |
|------|---------|------|------|
| 基础 SMP | 4.x+ | ✅ | 4 核全开 |
| GPIO (pinctrl) | 4.x+ | ✅ | 完全支持 |
| UART | 4.x+ | ✅ | 6 路 UART |
| I²C | 4.x+ | ✅ | 4 路 TWI |
| SPI | 4.x+ | ✅ | sun6i-spi 驱动 |
| MMC/SDIO | 4.x+ | ✅ | SD 卡 + WiFi SDIO |
| USB OTG/HOST | 4.x+ | ✅ | FEL + Host |
| DMA | 4.x+ | ✅ | 内存搬运 |
| PWM | 4.x+ | ✅ | sunxi-pwm |
| Watchdog | 4.x+ | ✅ | 看门狗 |
| RTC | 4.x+ | ✅ | 实时时钟 |
| Audio Codec | 4.x+ | ✅ | 音频输出 |
| NAND | 5.x+ | ⚠️ | 部分支持，需特定配置 |
| Mali GPU (Lima) | 5.2+ | ⚠️ | 开源驱动，实验性 |
| Video Decode (cedrus) | 5.x+ | ⚠️ | 硬件解码，实验性 |

---

## 开发流程

### 获取内核

```bash
# 使用主线内核（推荐）
git clone --depth 1 --branch v6.6 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
# 或使用 sunxi 开发分支（含未主线补丁）
git clone --depth 1 --branch sunxi/for-next https://github.com/linux-sunxi/linux.git
```

### 构建流程

```bash
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-

# 1. 使用 sunxi 默认配置
make sunxi_defconfig

# 2. 自定义配置（添加 R16 特定驱动）
make menuconfig

# 3. 构建
make -j$(nproc) zImage dtbs modules

# 4. 输出位置
# zImage: arch/arm/boot/zImage
# DTB: arch/arm/boot/dts/allwinner/sun8i-a33-*.dtb
# modules: 各驱动目录下的 .ko 文件
```

---

## 关键参考

- linux-sunxi Wiki：https://linux-sunxi.org/
- 主线内核 ARM Allwinner 文档：https://docs.kernel.org/arch/arm/sunxi.html
- R16 数据手册：https://linux-sunxi.org/images/b/b3/R16_Datasheet_V1.4_(1).pdf
- sunxi Mail List：https://groups.google.com/g/linux-sunxi
