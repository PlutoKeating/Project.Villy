# 🚀 快速入门：连接与刷写实战指南

> 本文档提供从零开始连接 CRL200S 机器人、获取 Shell、备份固件、刷写系统的完整实战流程。

---

## 0. 前置准备

### PC 端工具安装

```bash
# ===== Ubuntu/Debian =====
# ADB (Android Debug Bridge)
sudo apt install adb

# sunxi-tools (FEL 刷写工具)
sudo apt install sunxi-tools
# 或从源码编译：git clone https://github.com/linux-sunxi/sunxi-tools.git && cd sunxi-tools && make && sudo make install

# 固件分析工具
sudo apt install binwalk squashfs-tools device-tree-compiler

# ===== macOS =====
brew install android-platform-tools sunxi-tools binwalk

# ===== Windows =====
# ADB: 下载 Android SDK Platform Tools
# sunxi-fel: 需用 WSL2 或从 linux-sunxi 源码编译
```

### 硬件准备

| 物品 | 要求 |
|------|------|
| Micro USB 数据线 | ⚠️ 必须是**数据传输线**（不能是纯充电线！） |
| PC | Linux / macOS / Windows(WSL2) |
| 机器人 | 已拆机，主板 CRL200S Micro USB 口可见 |

---

## 1. 连接机器人 — 获取 Shell

### 1.1 通过 ADB 获取 Root Shell

```bash
# ===== 步骤 1: 物理连接 =====
# 用 Micro USB 数据线连接主板的 Micro USB 口到 PC

# ===== 步骤 2: 启动机器人，等待 30-60 秒开机 =====

# ===== 步骤 3: 检查 ADB 连接 =====
adb devices
# 期望输出:
# List of devices attached
# 0123456789ABCDEF    device

# 如果显示 "unauthorized" → 机器人屏幕上可能需要确认
# 如果显示 "no devices" → 见 1.2 节

# ===== 步骤 4: 进入 Shell =====
adb shell
# 你应该看到 root 提示符:
# root@rockrobo:/#
```

**恭喜！你现在已经在机器人内部了。** 从这里开始可以做任何事情：查看分区、备份固件、传输文件、安装软件。

### 1.2 ADB 不识别怎么办

部分 CRL200S 机型在启动后快速关闭 ADB 服务。使用专用工具捕获：

```bash
# 下载 CRL200S ADB 启用工具
git clone https://github.com/Hypfer/valetudo-crl200s-root.git
cd valetudo-crl200s-root

# 运行脚本（会在开机瞬间捕获 ADB 窗口）
chmod +x enable-adb.sh
./enable-adb.sh

# 按照脚本提示操作：
# 1. 断开 USB
# 2. 关闭机器人
# 3. 重新开机
# 4. 立即插入 USB
# 5. 脚本会自动检测并启用 ADB
```

### 1.3 通过 ADB 传输文件

```bash
# 从 PC 上传文件到机器人
adb push ./my-script.sh /data/local/tmp/

# 从机器人下载文件到 PC
adb pull /data/local/tmp/sensor-log.txt ./

# 在机器人和 PC 之间同步目录
adb sync /data/local/backups/ ./local-backups/
```

---

## 2. 备份固件 — 保护你的后路

> ⚠️ **在刷入任何东西之前，必须完整备份！** 这是唯一的后悔药。

### 2.1 方法一：在线备份 (ADB Shell → dd) ⭐ 推荐

不需要进入 FEL 模式，直接在 ADB Shell 中操作：

```bash
# 进入 ADB Shell
adb shell

# === 在机器人内部执行 ===

# 1. 查看分区布局
cat /proc/mtd
# 输出示例:
# dev:    size   erasesize  name
# mtd0: 00100000 00020000 "bootloader"
# mtd1: 00800000 00020000 "kernel"
# mtd2: 0f000000 00020000 "rootfs"
# mtd3: 08000000 00020000 "app"
# mtd4: 04000000 00020000 "data"

# 2. 逐个备份每个分区
mkdir -p /data/local/tmp/backup
for part in mtd0 mtd1 mtd2 mtd3 mtd4; do
    echo "Backing up $part..."
    dd if=/dev/$part of=/data/local/tmp/backup/${part}.img bs=4096
done

# 3. 校验备份
md5sum /data/local/tmp/backup/*.img > /data/local/tmp/backup/md5sums.txt

# 4. 下载到 PC
exit  # 退出 shell
adb pull /data/local/tmp/backup/ ./nand-backup/

# 5. 验证 PC 端文件完整性
cd nand-backup
md5sum -c md5sums.txt
```

### 2.2 方法二：FEL 离线备份 (sunxi-fel)

需要进入 FEL 模式（见第 3 节），然后：

```bash
# 一次性完整 dump（推荐）
sudo sunxi-fel nand-read 0 0x20000000 nand-full-backup.bin
#                                  ↑ offset    ↑ 512MB

# 或按分区 dump（更灵活）
sudo sunxi-fel nand-read 0x00000000 0x00100000 mtd0-bootloader.img
sudo sunxi-fel nand-read 0x00280000 0x00800000 mtd1-kernel.img
# ... 根据实际分区布局调整偏移量和大小

# 验证备份
md5sum nand-full-backup.bin
```

### 2.3 必须备份的额外数据

| 数据 | 命令 | 说明 |
|------|------|------|
| SoC SID | `adb shell "cat /sys/class/sunxi_info/sys_info"` | 芯片唯一 ID |
| WiFi MAC | `adb shell "cat /data/misc/wifi/config"` | MAC 地址 |
| 序列号 | 机器人底部贴纸 | 设备身份 |
| 原厂设备树 | `adb pull /sys/firmware/fdt ./original-fdt.dtb` | DTB 文件 |

---

## 3. 进入 FEL 模式 — 低级刷写的钥匙

FEL 模式允许通过 USB 直接读写 NAND Flash，不依赖任何已安装的系统。

### 3.1 方法 A：从 ADB Shell 进入（首选）

```bash
# 在 ADB Shell 中
adb shell

# 方法 1: 直接重启到 FEL
reboot fel
# 部分系统支持此命令，机器人会重启进入 FEL

# 方法 2: 重启到 bootloader
reboot bootloader
# 然后在 U-Boot 提示符下输入:
# => fel
```

### 3.2 方法 B：NAND 物理短接法（备选）

如果系统无法正常启动：

1. 找到主板上的 NAND Flash 芯片（通常为 TSOP-48 封装）
2. 用镊子或 100Ω 电阻短接 NAND 的 D0 和 D1 引脚
3. 通电开机
4. SoC 无法读取 NAND → 自动回退到 FEL 模式
5. PC 端确认：`sudo sunxi-fel version`

### 3.3 验证 FEL 连接

```bash
# 检测 FEL 设备
sudo sunxi-fel --list --verbose

# 读取 SoC 信息（应显示 A33）
sudo sunxi-fel version
# AWUSBFEX soc=1667(A33) ver=0001 44 08 scratchpad=00017e00 00000000 00000000

# 如果显示 "No Allwinner FEL device found":
# 1. 确认 USB 线是数据线
# 2. 确认机器人已关闭再开机（或短接了 NAND）
# 3. 尝试不同 USB 口
# 4. 加 sudo
```

---

## 4. 刷写自定义系统

### 4.1 FEL Boot — 内存执行（安全测试，不写入 NAND）

适合在不破坏原厂系统的情况下快速测试内核：

```bash
# 1. 将自定义内核加载到内存并执行
sudo sunxi-fel write 0x42000000 zImage           # 内核
sudo sunxi-fel write 0x43000000 sun8i-a33-crl200s.dtb  # 设备树
sudo sunxi-fel write 0x44000000 initramfs.cpio.gz      # 最小 rootfs
sudo sunxi-fel exec 0x42000000                   # 启动!

# 机器人在内存中运行你的 Linux，重启后恢复原厂系统
```

### 4.2 刷写 U-Boot 到 NAND

```bash
# 编译主线 U-Boot 后
sudo sunxi-fel nand-write 0x0 u-boot-sunxi-with-spl.bin
# SPL 和 U-Boot 被写入 NAND 第 0 块
```

### 4.3 刷写完整系统镜像

```bash
# 写入内核到 boot 分区
sudo sunxi-fel nand-write 0x280000 zImage

# 写入 rootfs 到对应分区
sudo sunxi-fel nand-write 0xA80000 rootfs.squashfs

# 或一次性写入完整系统
sudo sunxi-fel nand-write 0x0 full-system-image.img
```

---

## 5. 完整操作流程速查

```
┌───────────────────────────────────────────────────────┐
│              首次操作 CRL200S 的标准流程                │
├───────────────────────────────────────────────────────┤
│                                                       │
│  [1] Micro USB 线连接 PC ↔ 机器人                      │
│       │                                               │
│  [2] 开机，adb devices 检查连接                         │
│       │                                               │
│  [3] adb shell 进入 root shell                        │
│       │                                               │
│  [4] cat /proc/mtd 查看分区布局                        │
│       │                                               │
│  [5] dd 备份所有分区 → adb pull 到 PC 保存              │
│       │                                               │
│  [6] 保存 WiFi MAC、序列号、SID                        │
│       │                                               │
│  [7] reboot fel 进入 FEL 模式                          │
│       │                                               │
│  [8] sunxi-fel nand-read 完整 dump (二次保险)           │
│       │                                               │
│  [9] 开始安全地实验！                                   │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## 6. 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `adb devices` 无设备 | USB 线是充电线 | 换一根确定能传数据的 Micro USB 线 |
| `adb devices` 显示 `unauthorized` | 需要授权 | 机器人屏幕上可能弹出确认框（部分机型无屏幕则跳过） |
| ADB 闪现后消失 | 系统关闭了 ADB | 用 `enable-adb.sh` 捕获开机窗口 |
| `sunxi-fel` 找不到设备 | 未进入 FEL 模式 | 先 `adb shell reboot fel` 或 NAND 短接 |
| `nand-read` 失败 | NAND 时序问题 | 尝试不同的块大小或使用 `dd` 方法代替 |
| rootfs 写入后无法启动 | 分区布局不匹配 | 从备份的 `/proc/mtd` 确认实际分区偏移量 |

---

## 7. 参考资源

| 资源 | 说明 |
|------|------|
| [1.4 调试接口](../hardware/docs/reference/04-debug/README.md) | 硬件接口详情 |
| [2.2 FEL 刷写指南](../firmware/docs/reference/02-fel/README.md) | FEL 详细操作 |
| [2.10 固件提取](../firmware/docs/reference/10-extraction/README.md) | 固件分析方法 |
| [valetudo-crl200s-root](https://github.com/Hypfer/valetudo-crl200s-root) | ADB 启用工具 |
| [sunxi-tools](https://github.com/linux-sunxi/sunxi-tools) | FEL 刷写工具 |
| [linux-sunxi FEL](https://linux-sunxi.org/FEL) | FEL 协议文档 |

---

*本指南适用于所有基于 3irobotix CRL200S 主板的扫地机器人。*
