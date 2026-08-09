# 2.6 Debian armhf 移植

> 在 SDJQR02RR 上运行完整 Debian armhf 系统，提供丰富的软件包生态。

---

## armhf 架构说明

Debian **armhf**（ARM Hard Float）是 Debian 对 ARMv7 硬浮点架构的官方移植：

- 支持 ARM Cortex-A 系列（含 R16 的 Cortex-A7）
- 使用硬件浮点 VFPv3/v4 + NEON
- 软件包数量与 x86 相当（~60000+ 包）
- 正在积极维护（Debian 12 Bookworm, 13 Trixie）

---

## 构建方法

### 方法一：debootstrap（推荐）

```bash
# 安装 debootstrap
sudo apt install debootstrap qemu-user-static

# 创建 armhf rootfs（Debian 12 Bookworm）
sudo debootstrap --arch=armhf --foreign bookworm debian-armhf http://deb.debian.org/debian

# 复制 qemu 到 rootfs（用于在 x86 主机上执行 arm 二进制）
sudo cp /usr/bin/qemu-arm-static debian-armhf/usr/bin/

# 完成第二阶段安装
sudo chroot debian-armhf /debootstrap/debootstrap --second-stage
```

### 方法二：multistrap

```bash
# 更精细的包选择
sudo apt install multistrap
cat > multistrap.conf << EOF
[General]
arch=armhf
directory=debian-armhf
cleanup=true
unpack=true

[Debian]
packages=systemd udev bash login passwd netbase
         sysvinit-utils iproute2 dhcpcd5
         openssh-server python3 python3-pip
         wpasupplicant wireless-tools
         i2c-tools spi-tools
source=http://deb.debian.org/debian bookworm main
EOF

sudo multistrap -f multistrap.conf
```

---

## 配置系统

### 基础配置

```bash
# chroot 进入
sudo chroot debian-armhf

# 设置 root 密码
passwd

# 设置 hostname
echo "villy" > /etc/hostname

# 配置网络
cat > /etc/network/interfaces << EOF
auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet dhcp
    wpa-ssid YOUR_WIFI_SSID
    wpa-psk YOUR_WIFI_PASSWORD
EOF

# 启用 SSH
systemctl enable ssh

# 创建用户
useradd -m -s /bin/bash pk
passwd pk
```

### 精简系统（节省空间）

```bash
# 删除不必要的文档和 locale
find /usr/share/doc -type f -delete
find /usr/share/locale -mindepth 1 -maxdepth 1 ! -name 'en*' -exec rm -rf {} +

# 删除不需要的服务
systemctl disable bluetooth.service
systemctl disable avahi-daemon.service

# 使用 apt 清理
apt clean
apt autoremove --purge
```

---

## 内核与模块

Debian rootfs 需要与自行编译的内核配合：

```bash
# 在宿主机上编译内核
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules_install INSTALL_MOD_PATH=/path/to/debian-armhf
```

---

## 部署

### 打包 rootfs

```bash
# 创建压缩包
sudo tar -C debian-armhf -czf villy-debian-armhf.tar.gz .

# 或创建 ext4 镜像
sudo dd if=/dev/zero of=villy-rootfs.ext4 bs=1M count=512
sudo mkfs.ext4 villy-rootfs.ext4
sudo mount villy-rootfs.ext4 /mnt
sudo cp -a debian-armhf/* /mnt/
sudo umount /mnt
```

### 刷写

```bash
# 通过 FEL 写入 NAND
sudo sunxi-fel nand-write 0x1000000 villy-rootfs.ext4

# 或使用 U-Boot + tftp/usb
```

---

## 交叉编译 Python 软件包

```bash
# 在 rootfs 中安装
sudo chroot debian-armhf pip3 install flask flask-sock pyserial smbus2

# 或使用 piwheels（ARMv7 预编译 Python 包的仓库）
# 在目标设备上：
pip3 install --index-url https://www.piwheels.org/simple flask
```

**piwheels** 是 ARM 平台 Python 包的预编译仓库，可大幅减少在设备上编译 Python C 扩展的时间：https://www.piwheels.org/

---

## 系统服务示例

### villy-hal.service

```ini
[Unit]
Description=Villy Hardware Abstraction Layer
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/villy
ExecStart=/usr/bin/python3 -m backend.app.main
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 参考资源

- Debian armhf 移植：https://wiki.debian.org/ArmHardFloatPort
- debootstrap 文档：https://wiki.debian.org/Debootstrap
- piwheels：https://www.piwheels.org/
- ARM 嵌入式 Linux 指南（Jay Carlson）：https://jaycarlson.net/embedded-linux/
