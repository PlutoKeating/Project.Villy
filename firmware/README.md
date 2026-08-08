# Firmware 固件与刷写

> 本模块负责 SDJQR01RR 的交叉编译工具链管理、内核构建、rootfs 创建和刷写流程。

## 工作范围

- Allwinner R16 交叉编译工具链（ARMv7）
- 主线 Linux (sunxi) 内核适配
- 设备树 (DTS) 编写
- Buildroot / Debian rootfs 构建
- 刷写脚本与流程文档
- 驱动模块编译与验证

## 目录结构

```
firmware/
├── README.md               # 本文件
├── docs/
│   ├── build-guide.md      # 完整构建指南
│   ├── flashing-guide.md   # 刷写流程
│   ├── flashing-log.md     # 刷写操作记录
│   └── driver-validation.md # 驱动验证报告
├── configs/                # 内核 .config
├── dts/                    # 设备树源文件
├── patches/                # 内核补丁
├── submodules/             # git submodule（外部工具链）
└── images/                 # 构建产物（不入库）
```

## 快速入口

| 文档 | 内容 |
|------|------|
| [构建指南](docs/build-guide.md) | 交叉编译环境搭建与构建步骤 |
| [刷写流程](docs/flashing-guide.md) | FEL 模式刷写 NAND / SD 启动 |
| [刷写记录](docs/flashing-log.md) | 每次刷写操作的四要素记录 |
| [驱动验证](docs/driver-validation.md) | GPIO/I2C/SPI/PWM 驱动测试 |

## 外部工具链 (submodule)

通过 `git submodule` 引入，固定到已知可用的 commit：

- `sunxi-tools` — Allwinner FEL 模式刷写工具
- `linux` — 主线 sunxi 内核
- `buildroot` — 最小 rootfs 构建系统

添加方式：
```bash
git submodule add https://github.com/linux-sunxi/sunxi-tools.git firmware/submodules/sunxi-tools
git submodule add --depth 1 --branch sunxi/for-next https://github.com/linux-sunxi/linux.git firmware/submodules/linux
```

---

> 所有操作记录严格遵循 [AGENT.md](../../AGENT.md) 中定义的「发现→方案→结果→复盘」四要素规范。
