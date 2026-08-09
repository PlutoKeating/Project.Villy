# 5.1 GitHub 相关项目索引

---

## CRL200S 专项项目 ⭐

### codetiger/VacuumRobot
- **仓库**: https://github.com/codetiger/VacuumRobot
- **语言**: 文档 + 研究资料
- **说明**: **CRL200S 完整逆向工程** — 元器件图、连接验证、协议分析、固件实验
- **关键内容**:
  - Motherboard/Component_Diagram.md — 每个芯片的丝印和连接关系
  - Motherboard/Connection_Evidence.md — 验证过的引脚连接
  - Research/GD32F1/README.md — A33↔GD32 UART3 通信协议
  - Research/Software/Firmware/ — 早期 Rust 固件实验
- **对 Villy 的价值**: ⭐⭐⭐⭐⭐ 最核心的硬件参考

### codetiger/VacuumTiger
- **仓库**: https://github.com/codetiger/VacuumTiger
- **语言**: Rust
- **说明**: **CRL200S 开源替代固件** — 包含 SangamIO 守护进程、Drishti 诊断 UI、TCP SLAM 协议
- **对 Villy 的价值**: 固件架构参考，驱动实现参考

### Hypfer/valetudo-crl200s-root
- **仓库**: https://github.com/Hypfer/valetudo-crl200s-root
- **语言**: Shell
- **说明**: **CRL200S ADB root 工具** — 一键启用 ADB 访问，获取 root shell
- **对 Villy 的价值**: 调试入口工具

### RoombaMaster/VacuumRobotLidarMapMaker
- **仓库**: https://github.com/RoombaMaster/VacuumRobotLidarMapMaker
- **说明**: CRL200S 激光雷达建图项目
- **对 Villy 的价值**: LDS 数据协议参考

---

## 扫地机器人通用项目

### Valetudo
- **仓库**: https://github.com/Hypfer/Valetudo
- **Stars**: 15,000+
- **说明**: 扫地机器人去云端固件
- **对 Villy 的价值**: 架构参考，MQQT 集成模式

### Dustcloud (文档仓库)
- **仓库**: https://github.com/dgiese/dustcloud-documentation
- **说明**: 小米 IoT 设备硬件文档（含部分 CRL200S 资料）
- **对 Villy 的价值**: PCB 照片，UART 日志

### Dustbuilder
- **网站**: https://builder.dontvacuum.me/
- **说明**: 在线定制 root 固件
- **对 Villy 的价值**: 快速验证 root 可行性

### awesome-vacuum
- **仓库**: https://github.com/awesome-vacuum/awesome-vacuum
- **说明**: 开源扫地机器人资源精选列表

---

## Allwinner / sunxi 项目

| 项目 | URL | 说明 |
|------|-----|------|
| linux-sunxi/linux-sunxi | https://github.com/linux-sunxi/linux-sunxi | sunxi 内核 |
| linux-sunxi/sunxi-tools | https://github.com/linux-sunxi/sunxi-tools | FEL 工具集 |
| armbian/build | https://github.com/armbian/build | Armbian 构建系统 |

---

## 嵌入式 Linux 构建

| 项目 | URL | 说明 |
|------|-----|------|
| buildroot/buildroot | https://github.com/buildroot/buildroot | Buildroot |
| u-boot/u-boot | https://github.com/u-boot/u-boot | 主线 U-Boot |

---

## 机器人中间件

| 项目 | URL | 说明 |
|------|-----|------|
| micro-ROS/micro-ROS | https://github.com/micro-ROS | MCU ROS 2 |
| RobotWebTools | https://github.com/RobotWebTools | Web 机器人工具 |

---

## Home Assistant 集成

- Home Assistant Community — Valetudo 讨论: https://community.home-assistant.io/
- Makers Pet CRL200S→ROS2 教程: https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/
