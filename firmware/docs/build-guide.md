# 构建指南

> 本文档描述从源码构建适用于 SDJQR01RR 的 Linux 内核和 rootfs 的完整流程。

## 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| arm-linux-gnueabihf-gcc | ≥ 10 | ARMv7 交叉编译器 |
| make | ≥ 4.0 | 构建工具 |
| device-tree-compiler | ≥ 1.5 | DTS → DTB |
| python3 | ≥ 3.14 | sunxi-tools 等脚本依赖 |
| libusb-1.0-0-dev | — | FEL 刷写工具依赖 |

## 步骤

### 1. 获取源码

```bash
cd firmware/submodules
git submodule update --init --recursive
```

### 2. 编译 sunxi-tools

```bash
cd firmware/submodules/sunxi-tools
make -j$(nproc)
```

### 3. 编译内核

```bash
cd firmware/submodules/linux
cp ../../configs/kernel.config .config
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc) zImage dtbs modules
```

### 4. 构建 rootfs (Buildroot)

```bash
cd firmware/submodules/buildroot
cp ../../configs/buildroot.config .config
make -j$(nproc)
```

### 5. 打包刷写镜像

```bash
# 见 flashing-guide.md
```

---

*待实际构建验证后更新具体命令和输出。*
