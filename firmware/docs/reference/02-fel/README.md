# 2.2 FEL 模式刷写深度指南

> FEL（Failsafe Engine Loader）是 Allwinner BootROM 的低级 USB 恢复模式，是初始刷写的核心工具。

---

## FEL 原理

当 Allwinner SoC 上电后，BootROM 按以下顺序尝试启动：

```
1. SPI NOR Flash → 2. NAND Flash → 3. SD Card → 4. FEL (fallback)
```

如果前三种介质都无法正常读取（空芯片、数据损坏或人为短路数据线），BootROM 回退到 **FEL 模式**，通过 USB OTG 接口暴露一个简单的通信协议。

### FEL 协议能力

| 操作 | 说明 |
|------|------|
| `ver` | 读取 SoC 型号和版本 |
| `read` | 读取任意内存地址 |
| `write` | 写入任意内存地址 |
| `exec` | 跳转到指定地址执行代码 |
| `spiflash-read` | 读取 SPI NOR Flash |
| `spiflash-write` | 写入 SPI NOR Flash |
| `nand-read` | 读取 NAND Flash |
| `nand-write` | 写入 NAND Flash |
| `sid` | 读取芯片唯一 ID |

---

## sunxi-fel 安装与使用

### 安装

```bash
# 从源码编译
git clone https://github.com/linux-sunxi/sunxi-tools.git
cd sunxi-tools
make
sudo make install

# 或包管理器安装
sudo apt install sunxi-tools    # Debian/Ubuntu
```

### 检测设备

```bash
# 查看所有连接的 FEL 设备
sudo sunxi-fel --list --verbose

# 读取 SoC 信息
sudo sunxi-fel version
# 输出：AWUSBFEX soc=1667(R16) ver=0001 44 08 scratchpad=00017e00 00000000 00000000
```

---

## 核心操作流程

### 1. 备份原厂 NAND（关键步骤！）

```bash
# 读取 NAND 完整镜像到文件
sudo sunxi-fel nand-read 0 0x20000000 nand-backup.bin
#                    ↑offset ↑size(512MB) ↑输出文件

# 验证备份完整性
md5sum nand-backup.bin
```

### 2. FEL Boot（无需刷写，仅内存执行）

```bash
# 写入内核到内存
sudo sunxi-fel write 0x42000000 zImage

# 写入设备树
sudo sunxi-fel write 0x43000000 sun8i-a33-sdjqr02rr.dtb

# 写入 initramfs
sudo sunxi-fel write 0x44000000 initramfs.cpio.gz

# 跳转执行（参数：内核地址、DTB地址）
sudo sunxi-fel exec 0x42000000
```

### 3. 刷写 U-Boot 到 NAND

```bash
# 写入 SPL + U-Boot
sudo sunxi-fel nand-write 0x0 u-boot-sunxi-with-spl.bin
```

### 4. 刷写完整系统

```bash
# 写入内核
sudo sunxi-fel nand-write 0x800000 zImage

# 写入 rootfs
sudo sunxi-fel nand-write 0x1000000 rootfs.squashfs
```

---

## 进入 FEL 的实践方法（小米扫地机专项）

### 方法一：NAND 数据线短路法（最可靠）

1. 拆机，找到 NAND Flash 芯片
2. 在 NAND 数据线（D0-D7）中任意两脚之间焊接一个 100Ω 电阻或短接
3. 通电，SoC 无法读取 NAND → 进入 FEL
4. USB 连接 PC，确认 `sunxi-fel version` 检测到设备
5. 操作完成后移除短路

**注意**：操作要快，避免长时间短路导致芯片过热。

### 方法二：FEL 按钮（如果存在）

部分设备在 PCB 上有 FEL 测试点或按钮。拆机后寻找标记为 `FEL`、`BOOT` 或 `RECOVERY` 的焊盘。

---

## 社区实战记录

- **Hackaday (2019)**：通过短路 NAND 数据线进入 FEL，dump 小米扫地机 MMC 存储
- **Dustbuilder FEL 固件**：dgiese 提供基于 FEL 的 autoroot 方案，无需实际刷写 NAND
- **4PDA 论坛**：大量俄语用户分享 FEL 刷写经验

---

## 常见问题

| 问题 | 解决 |
|------|------|
| `No Allwinner FEL device found` | 检查 USB 线、确认设备已进入 FEL、尝试 `sudo` |
| FEL 连接后立即断开 | USB 供电不足，使用带外部供电的 USB Hub |
| `nand-read` 失败 | NAND 访问时序可能特殊，尝试不同偏移量 |
| 操作中设备断开 | 检查短路连接是否稳定 |

---

## 参考资源

- linux-sunxi FEL 文档：https://linux-sunxi.org/FEL
- sunxi-tools 手册：https://github.com/linux-sunxi/sunxi-tools
- OpenCentauri FEL 指南：https://docs.opencentauri.cc/software/FEL-mode/
- PhoenixSuit 指南（Windows 替代）：https://flashguidehub.com/phoenixsuit/
