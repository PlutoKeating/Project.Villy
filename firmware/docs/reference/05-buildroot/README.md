# 2.5 Buildroot 最小系统构建

> 使用 Buildroot 构建适用于 SDJQR02RR 的最小 Linux 系统。

---

## Buildroot 简介

Buildroot 是一套 Makefile + 补丁的集合，用于自动化生成嵌入式 Linux 系统。核心特点：

- **输出完整系统**：cross-compilation toolchain、root filesystem、kernel image、bootloader
- **极致轻量**：最小 busybox 系统 ≈ 1.5MB
- **配置简单**：`make menuconfig` 图形界面
- **可重现构建**：固定版本的源码和配置

---

## 获取 Buildroot

```bash
git clone --depth 1 --branch 2024.02 https://github.com/buildroot/buildroot.git
cd buildroot
```

## 配置流程

```bash
# 1. 加载默认配置（Allwinner ARM）
make sunxi_defconfig

# 2. 进入 menuconfig 调整
make menuconfig
```

### 关键配置项

```ini
# Target options
BR2_arm=y
BR2_cortex_a7=y
BR2_ARM_FPU_NEON_VFPV4=y
BR2_SOFT_FLOAT=y               # → n, 使用硬浮点（推荐）
BR2_TARGET_GENERIC_HOSTNAME="villy"
BR2_TARGET_GENERIC_ISSUE="Welcome to Project.Villy"

# Toolchain
BR2_KERNEL_HEADERS_6_1=y       # 匹配内核版本
BR2_GCC_VERSION_12_X=y

# System configuration
BR2_SYSTEM_BIN_SH_BUSYBOX=y
BR2_TARGET_GENERIC_GETTY_PORT="ttyS0"
BR2_TARGET_GENERIC_GETTY_BAUDRATE_115200=y
BR2_ROOTFS_POST_BUILD_SCRIPT="board/villy/post-build.sh"

# Kernel
BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_CUSTOM_GIT=y
BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/linux-sunxi/linux.git"
BR2_LINUX_KERNEL_CUSTOM_REPO_VERSION="sunxi/for-next"
BR2_LINUX_KERNEL_DEFCONFIG="sunxi"

# Filesystem images
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_SQUASHFS=y
BR2_TARGET_ROOTFS_TAR=y

# 可选软件包
BR2_PACKAGE_PYTHON3=y           # Python 3
BR2_PACKAGE_PYTHON_FLASK=y      # Flask（需手动添加）
BR2_PACKAGE_DROPBEAR=y          # SSH server（轻量）
BR2_PACKAGE_I2C_TOOLS=y         # i2cdetect/i2cget/i2cset
BR2_PACKAGE_SPI_TOOLS=y         # spidev 测试
BR2_PACKAGE_WPA_SUPPLICANT=y    # WiFi 管理
```

---

## 板级定制

创建 `board/villy/` 目录：

```bash
board/villy/
├── post-build.sh       # 构建后脚本
├── post-image.sh       # 镜像生成后脚本
├── rootfs_overlay/     # rootfs 覆盖文件
│   ├── etc/
│   │   ├── network/interfaces
│   │   └── wpa_supplicant.conf
│   └── etc/init.d/S99villy  # 自启动脚本
├── linux.fragment      # 内核额外配置片段
└── genimage.cfg        # 镜像打包配置
```

### post-build.sh 示例

```bash
#!/bin/sh
# 设置 hostname
echo "villy" > $TARGET_DIR/etc/hostname

# 复制 WiFi 配置
cp board/villy/rootfs_overlay/etc/wpa_supplicant.conf $TARGET_DIR/etc/

# 启用自动登录
sed -i 's/.*ttyS0.*/ttyS0::respawn:\/sbin\/getty -L ttyS0 115200 vt100/'     $TARGET_DIR/etc/inittab
```

---

## 构建

```bash
cd buildroot
make -j$(nproc)
```

### 构建产物

```
output/images/
├── zImage                         # Linux 内核
├── sun8i-a33-sdjqr02rr.dtb        # 设备树
├── rootfs.squashfs                # squashfs rootfs
├── rootfs.ext2                    # ext2 rootfs
├── rootfs.tar                     # rootfs tar（部署用）
└── boot.scr                       # U-Boot 启动脚本
```

---

## 部署到设备

### FEL Boot（临时测试）

```bash
sudo sunxi-fel write 0x42000000 output/images/zImage
sudo sunxi-fel write 0x43000000 output/images/sun8i-a33-sdjqr02rr.dtb
sudo sunxi-fel write 0x44000000 output/images/rootfs.squashfs
sudo sunxi-fel exec 0x42000000
```

### 刷写到 NAND（永久）

```bash
sudo sunxi-fel nand-write 0x0 output/images/u-boot-sunxi-with-spl.bin
# 通过 U-Boot 将 rootfs 写入 NAND 分区
```

---

## Buildroot vs 其他方案

| 维度 | Buildroot | Yocto | Debian armhf |
|------|-----------|-------|-------------|
| 构建时间 | ~30min | ~2-4h | — |
| 镜像大小 | ~5-20MB | ~20-100MB | ~200MB+ |
| 学习曲线 | 低 | 高 | 低 |
| 定制化 | 高 | 极高 | 低 |
| 软件包数量 | ~2500 | ~∞ | ~60000 |
| 适合阶段 | 原型验证 | 产品化 | 开发环境 |

**推荐路径**：Buildroot（原型验证）→ Debian armhf（开发环境）→ Buildroot/Yocto（最终优化）

---

## 参考资源

- Buildroot 官方手册：https://buildroot.org/downloads/manual/manual.html
- linux-sunxi Buildroot 指南：https://linux-sunxi.org/Buildroot
- Buildroot Allwinner F1C100s 教程：https://qyx.krtko.org/tutorials/f1c100s.html
- Buildroot allwinner_defconfig 参考
