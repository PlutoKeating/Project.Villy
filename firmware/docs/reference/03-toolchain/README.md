# 2.3 交叉编译工具链

> 为 Allwinner R16 (ARMv7) 配置交叉编译环境，用于编译内核、U-Boot、Buildroot 和用户空间程序。

---

## 工具链选择

### 方案对比

| 方案 | 版本 | 优势 | 劣势 |
|------|------|------|------|
| **Linaro arm-linux-gnueabihf** | GCC 7-14 | 官方维护，稳定可靠 | 版本可能较旧 |
| **ARM 官方** | GCC 10-14 | 最新优化 | 下载需注册 |
| **Ubuntu/Debian 包** | GCC 12+ | `apt install` 方便 | 版本取决于发行版 |
| **Buildroot 自带** | 自动匹配 | 与 Buildroot 集成 | 仅限 Buildroot 内 |
| **crosstool-ng** | 自定义 | 精确控制 | 构建复杂 |

### 推荐方案

```bash
# 方案 A：使用 Linaro 预编译工具链（推荐入门）
wget https://releases.linaro.org/components/toolchain/binaries/latest-7/arm-linux-gnueabihf/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz
tar xf gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz
export PATH=$PWD/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf/bin:$PATH

# 方案 B：使用系统包管理器（Debian/Ubuntu）
sudo apt install gcc-arm-linux-gnueabihf binutils-arm-linux-gnueabihf
```

### 验证工具链

```bash
arm-linux-gnueabihf-gcc --version
# 输出：arm-linux-gnueabihf-gcc (Linaro GCC 7.5-2019.12) 7.5.0

# 测试编译
echo 'int main(){return 0;}' | arm-linux-gnueabihf-gcc -x c - -o /tmp/hello
file /tmp/hello
# 输出：ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked...
```

---

## 环境变量配置

```bash
# 添加到 ~/.bashrc 或固件模块工作脚本
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export PATH=/opt/arm-linux-gnueabihf/bin:$PATH

# 可选：并行编译线程数
export MAKEFLAGS="-j$(nproc)"
```

---

## 编译内核

```bash
cd linux/

# 清理
make mrproper

# 配置
make sunxi_defconfig

# 构建
make -j$(nproc) zImage dtbs modules

# 安装模块到临时目录
make INSTALL_MOD_PATH=/tmp/kernel-modules modules_install
```

## 编译 U-Boot

```bash
cd u-boot/

# 配置
make Sinovoip_BPI_M2_Plus_defconfig  # R16/A33 兼容配置

# 构建
make -j$(nproc)

# 输出：u-boot-sunxi-with-spl.bin
```

## 编译用户空间程序

```bash
# 静态链接（推荐用于 initramfs）
arm-linux-gnueabihf-gcc -static -o myapp myapp.c

# 动态链接（用于完整 rootfs）
arm-linux-gnueabihf-gcc -o myapp myapp.c
```

---

## R16 特定的 GCC 优化选项

```bash
# R16 是 Cortex-A7，支持 NEON SIMD
export CFLAGS="-mcpu=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=hard -O2"
export CXXFLAGS="$CFLAGS"
```

---

## 参考资源

- Linaro 工具链发布：https://releases.linaro.org/components/toolchain/binaries/
- ARM 开发者工具链：https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
- Buildroot 工具链文档：https://buildroot.org/downloads/manual/manual.html#_cross_compilation_toolchain
