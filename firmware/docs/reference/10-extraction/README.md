# 2.10 原厂固件提取与分析

> 在刷入自定义系统前，必须完整备份和分析原厂固件。这是最安全的逆向起点。

---

## 固件备份（最高优先级）

### 方法一：FEL NAND Dump

```bash
# 进入 FEL 模式后
sudo sunxi-fel nand-read 0 0x20000000 nand-full-backup.bin
# 512MB NAND 完整备份，约需 5-10 分钟
```

### 方法二：通过原厂系统

如果已有 root shell：
```bash
# 需要找到 NAND 设备节点
cat /proc/mtd
# dev:    size   erasesize  name
# mtd0: 00100000 00020000 "bootloader"
# mtd1: 00800000 00020000 "kernel"
# mtd2: 0f000000 00020000 "rootfs"
# ...

# 逐个 dump
for i in 0 1 2 3; do
    dd if=/dev/mtd$i of=nand-backup/mtd${i}.img bs=4096
done
```

### 备份清单

| 必须备份 | 说明 |
|----------|------|
| ✅ 完整 NAND 镜像 | 可以在任何情况下恢复 |
| ✅ 每个 mtd 分区 | 便于分析单个分区 |
| ✅ SoC SID/EFUSE | `sunxi-fel sid` |
| ✅ WiFi MAC 地址 | 原厂校准数据 |
| ✅ 设备唯一标识 | 序列号、did 等 |

---

## 分区布局分析

### 典型 Allwinner NAND 布局

| 分区名称 | 偏移 | 大小 | 内容 |
|----------|------|------|------|
| boot0 | 0x000000 | 1MB | BROM 代码（只读） |
| boot1 | 0x100000 | 1MB | 备份 boot0 |
| env | 0x200000 | 512KB | U-Boot 环境变量 |
| boot | 0x280000 | 8MB | kernel (zImage) |
| rootfs | 0xA80000 | 256MB | squashfs rootfs |
| app | — | 128MB | 厂商应用 + 语音包 |
| data | — | 64MB | 用户数据 |
| recovery | — | 8MB | 恢复系统 |

> 此布局为典型推测，实际需通过串口启动日志或 `mtdparts` 确认。

---

## 固件分析工具

### Binwalk

```bash
# 安装
sudo apt install binwalk

# 扫描固件
binwalk nand-full-backup.bin

# 提取
binwalk -e nand-full-backup.bin
```

### 内核镜像分析

```bash
# 识别压缩格式
file zImage
# zImage: Linux kernel ARM boot executable zImage (little-endian)

# 提取内核版本
strings zImage | grep "Linux version"
# Linux version 3.10.65 (gcc version 4.9.3) ...

# 提取内核配置（如果启用了 IKCONFIG）
scripts/extract-ikconfig zImage > kernel-config-backup
```

### 设备树分析

```bash
# 转换为可读格式
dtc -I dtb -O dts extracted.dtb > extracted.dts

# 搜索关键外设
grep -E 'uart|i2c|spi|pwm|gpio|wifi' extracted.dts
```

### rootfs 分析

```bash
# 挂载 squashfs（如果是）
sudo mount -t squashfs rootfs.img /mnt/rootfs -o loop

# 脱壳 unsquashfs
unsquashfs rootfs.img

# 分析启动脚本
ls squashfs-root/etc/init.d/
cat squashfs-root/etc/rc.local

# 找二进制文件
find squashfs-root -type f -executable | head -20
```

---

## 从原厂固件学习

通过分析原厂固件可以了解：

1. **硬件抽象**：厂商如何访问 GPIO、I²C、PWM
2. **传感器驱动**：IMU、LDS 等传感器的配置参数
3. **电机控制**：PWM 频率、占空比映射
4. **电源管理**：电池充电曲线、低功耗策略
5. **WiFi 配置**：AP 模式设置、配网流程

这些信息可以直接用在自定义 Linux 的驱动开发中。

---

## 参考资源

- Binwalk：https://github.com/ReFirmLabs/binwalk
- UBI/UBIFS 分析：`mtd-utils` 包（`ubinize`、`ubireader` 等）
- squashfs-tools：用于解压/打包 squashfs
- dtc（device-tree-compiler）：DTS ↔ DTB 转换
