# 第 2 章：固件与刷写参考

> 本章系统梳理 SDJQR02RR 的固件刷写全链路，从 sunxi 生态、FEL 工具链、交叉编译环境到内核构建、rootfs 创建和社区固件生态。

---

## 2.1 子章节导航

| 编号 | 文档 | 内容 |
|------|------|------|
| 2.1 | [sunxi 生态与主线内核](./01-sunxi/README.md) | linux-sunxi 社区、主线支持矩阵、关键仓库 |
| 2.2 | [FEL 模式刷写深度指南](./02-fel/README.md) | FEL 原理、sunxi-fel 使用、NAND dump/flash |
| 2.3 | [交叉编译工具链](./03-toolchain/README.md) | arm-linux-gnueabihf 工具链获取、配置、使用 |
| 2.4 | [内核配置与设备树](./04-kernel/README.md) | 内核 .config、DTS 编写、驱动开发 |
| 2.5 | [Buildroot 最小系统构建](./05-buildroot/README.md) | Buildroot 配置、最小 rootfs、init 系统 |
| 2.6 | [Debian armhf 移植](./06-debian/README.md) | debootstrap、multistrap、预构建镜像 |
| 2.7 | [Valetudo 生态调研](./07-valetudo/README.md) | Valetudo 架构、支持设备、刷入方法 |
| 2.8 | [Dustcloud/Dustbuilder 工具链](./08-dustcloud/README.md) | MITM 代理、Dustbuilder 定制固件 |
| 2.9 | [U-Boot 引导加载器](./09-bootloader/README.md) | SPL、mainline U-Boot for sunxi |
| 2.10 | [原厂固件提取与分析](./10-extraction/README.md) | NAND dump、分区解析、文件系统提取 |

---

## 2.2 刷写方案总览

```
┌──────────────────────────────────────────────────────┐
│                    刷写方案决策树                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  原厂固件备份                                          │
│    │                                                 │
│    ├─ FEL 模式 → sunxi-fel → dump NAND → 安全保存     │
│    │                                                 │
│  刷入自定义 Linux                                      │
│    │                                                 │
│    ├─ 方案 A：轻量级                                   │
│    │   Buildroot → zImage + initramfs → FEL boot     │
│    │   适用：快速验证、驱动测试                           │
│    │                                                 │
│    ├─ 方案 B：中等重量                                 │
│    │   Buildroot → zImage + squashfs rootfs → NAND    │
│    │   适用：长期使用、有限存储                           │
│    │                                                 │
│    └─ 方案 C：完整 Linux                              │
│        Debian armhf → 完整 rootfs → NAND 或 SD 卡    │
│        适用：开发环境、ROS 2 评估                        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 2.3 关键仓库索引

| 仓库 | 用途 | URL |
|------|------|-----|
| linux-sunxi/linux-sunxi | sunxi 内核 | https://github.com/linux-sunxi/linux-sunxi |
| linux-sunxi/sunxi-tools | FEL 工具 | https://github.com/linux-sunxi/sunxi-tools |
| u-boot/u-boot | 主线 U-Boot | https://github.com/u-boot/u-boot |
| buildroot/buildroot | Buildroot | https://github.com/buildroot/buildroot |
| Hypfer/Valetudo | 去云端固件 | https://github.com/Hypfer/Valetudo |
| dgiese/dustcloud | MITM 代理 | https://github.com/dgiese/dustcloud |
| LibreRVAC | 开源扫地机固件 | https://github.com/LibreRVAC |
| codetiger/VacuumTiger | 开源扫地机固件 | https://github.com/codetiger/VacuumTiger |

---

*下一节：[2.1 sunxi 生态与主线内核](./01-sunxi/README.md)*
