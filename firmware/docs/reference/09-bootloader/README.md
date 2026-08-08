# 2.9 U-Boot 引导加载器

> 主线 U-Boot 已支持 Allwinner R16/A33。本节记录配置、编译和部署流程。

---

## U-Boot for Allwinner

主线 U-Boot 的 sunxi 平台支持包括：

- **SPL**（Secondary Program Loader）：初始化 DRAM，加载 U-Boot proper
- **U-Boot proper**：完整的引导加载器，支持网络、USB、存储
- **FEL**：U-Boot 可以通过 FEL 模式加载执行

### 构建流程

```bash
git clone --depth 1 https://github.com/u-boot/u-boot.git
cd u-boot

# 使用 Banana Pi M2 Magic 配置（R16/A33 兼容）
make Sinovoip_BPI_M2_Plus_defconfig

# 自定义（可选）
make menuconfig

# 构建
make CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
```

### 构建产物

```
u-boot-sunxi-with-spl.bin     # SPL + U-Boot 合并镜像（可直接刷写）
spl/sunxi-spl.bin              # 独立 SPL
u-boot.bin                     # 独立 U-Boot proper
u-boot.img                     # U-Boot 镜像格式
```

---

## U-Boot 配置关键项

```ini
CONFIG_ARM=y
CONFIG_ARCH_SUNXI=y
CONFIG_MACH_SUN8I_A33=y        # R16 使用 A33 代码
CONFIG_DEFAULT_DEVICE_TREE="sun8i-r16-sdjqr01rr"
CONFIG_SPL=y
CONFIG_SPL_SPI_SUNXI=y
CONFIG_MMC_SUNXI_SLOT_EXTRA=1  # SDIO WiFi
CONFIG_USB_MUSB_SUNXI=y
CONFIG_SYS_EXTRA_OPTIONS="CONS_INDEX=1"
CONFIG_BOOTCOMMAND="run boot_fel; run boot_mmc; run boot_nand"
```

---

## 启动流程

```
Power On
  │
  ▼
BROM (Boot ROM)
  │ 读取 NAND 第 0 块
  ▼
SPL (≤ 32KB)
  │ 初始化 DRAM、时钟
  ▼
U-Boot proper
  │ 初始化外设、网络
  ├── 自动启动（bootcmd）
  │      ├── boot_nand: 从 NAND 加载 kernel + DTB
  │      ├── boot_mmc:  从 SD 卡加载
  │      └── boot_fel:  FEL 网络启动
  ▼
Linux Kernel
```

---

## U-Boot 环境变量

```bash
# 从 NAND 启动
setenv boot_nand 'nand read 0x42000000 0x800000 0x500000; nand read 0x43000000 0x5800000 0x20000; bootz 0x42000000 - 0x43000000'

# 从 SD 卡启动
setenv boot_mmc 'fatload mmc 0 0x42000000 zImage; fatload mmc 0 0x43000000 sun8i-r16-sdjqr01rr.dtb; bootz 0x42000000 - 0x43000000'

# 从 FEL 网络启动（开发调试用）
setenv boot_fel 'tftp 0x42000000 zImage; tftp 0x43000000 sun8i-r16-sdjqr01rr.dtb; bootz 0x42000000 - 0x43000000'

# 保存
saveenv
```

---

## UART 控制台

启动时在串口终端按任意键进入 U-Boot 控制台：

```
U-Boot SPL 2024.01 (Jan 01 2024 - 00:00:00)
DRAM: 256 MiB
Trying to boot from NAND

U-Boot 2024.01 (Jan 01 2024 - 00:00:00 +0000)

CPU:   Allwinner R16 (SUN8I 1667)
Model: Xiaomi SDJQR01RR
DRAM:  256 MiB
NAND:  512 MiB
In:    serial@1c28000
Out:   serial@1c28000
Err:   serial@1c28000
Hit any key to stop autoboot:  0
=>
```

---

## 刷写 U-Boot

### 写入 NAND

```bash
# 通过 FEL
sudo sunxi-fel nand-write 0x0 u-boot-sunxi-with-spl.bin

# 或通过已有 U-Boot
=> nand erase 0x0 0x100000
=> nand write 0x42000000 0x0 0x80000
```

### 在 SD 卡上

```bash
sudo dd if=u-boot-sunxi-with-spl.bin of=/dev/sdX bs=1024 seek=8
```

---

## 社区经验

来自 linux-sunxi 邮件列表的讨论（Allwinner R16 U-Boot 主线）：

> 用户尝试从 SD 卡启动主线 U-Boot 到 R16，使用 `sudo dd if=uboot.img of=/dev/sdX bs=1024 seek=40`，但串口无输出。只有从原厂 BSP 提取的 100MB uboot.img 有效。

这说明 **R16 的主线 U-Boot 可能仍有兼容性问题**，需要在 SDJQR01RR 上实际测试。备选方案：
1. 使用原厂 U-Boot + 主线内核
2. 从原厂固件提取并修改 U-Boot 配置
3. 使用 sunxi 社区补丁版 U-Boot

---

## 参考资源

- 主线 U-Boot Allwinner 文档：https://docs.u-boot-project.org/en/latest/board/allwinner/sunxi.html
- linux-sunxi U-Boot 页面：https://linux-sunxi.org/U-Boot
- Google Groups 讨论：https://groups.google.com/g/linux-sunxi/c/hpxB29c9rB8
