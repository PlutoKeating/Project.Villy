# 2.8 Dustcloud / Dustbuilder 工具链

> Dennis Giese（dgiese）创建的小米 IoT 逆向工程工具链，是获取 root 权限和定制固件的核心工具。

---

## Dustcloud 项目

**GitHub**：https://github.com/dgiese/dustcloud

Dustcloud 是小米智能家居设备的 MITM（中间人）代理，最早用于分析小米扫地机器人与云端的通信协议。现已基本被 Valetudo 整合，但其**文档仓库**和**Dustbuilder 工具**仍然非常活跃。

### 核心组件

| 组件 | 说明 | 状态 |
|------|------|------|
| dustcloud | MITM 代理（Python） | 已整合到 Valetudo |
| dustcloud-documentation | 硬件文档仓库 | 持续更新 |
| dustbuilder | 在线定制 root 固件 | 在线运行 |
| dustbuilder-howto | 使用指南 | GitHub |

---

## Dustbuilder

**网址**：https://builder.dontvacuum.me/

Dustbuilder 是一个在线工具，用户输入设备信息后自动生成 root 固件镜像。支持：

- **Firmwarebuilder**：基于用户上传的原厂固件，自动注入 root 后门
- **FEL 固件**：通过 USB FEL 模式执行，无需刷写 NAND
- **Installer 固件**：已有 shell 权限时使用的安装器

### 使用流程（Dreame/3irobotix CRL200S）

1. 访问 https://builder.dontvacuum.me/
2. 选择设备型号（如 `dreame.crl200s`）
3. 上传对应版本的原厂固件
4. 选择需要的功能（Valetudo、SSH、WiFi 配置等）
5. 下载生成的定制固件
6. 通过 `miioOTA` 工具或 FEL 模式刷入

---

## Dennis Giese 的资源

| 资源 | URL | 说明 |
|------|-----|------|
| 个人主页 | https://dontvacuum.me/ | 项目入口 |
| GitHub | https://github.com/dgiese | 所有仓库 |
| Dustcloud 文档 | https://github.com/dgiese/dustcloud-documentation | PCB 照片、数据手册 |
| Dustbuilder | https://builder.dontvacuum.me/ | 在线固件构建 |
| 演讲稿（HITCON 2018） | https://hitcon.org/2018/CMT/slide-files/d2_s1_r0.pdf | 小米 IoT 逆向工程 |
| Telegram 频道 | @dust_announce | 更新公告 |

---

## 对 Project.Villy 的参考价值

1. **FEL 刷写方法**：Dustbuilder 的 FEL 固件方案可以直接借鉴
2. **固件注入技术**：如何在保持原厂功能的同时添加 root 访问
3. **硬件文档**：dustcloud-documentation 仓库包含大量小米设备的 PCB 照片和数据手册
4. **miIO 协议**：小米 IoT 设备的通信协议分析

---

## 关键发现：SDJQR02RR 的 Dustbuilder 支持

SDJQR02RR（Dreame/3irobotix CRL200S `dreame.crl200s`）是 Dustbuilder 最早支持的机型之一。这意味着：

- ✅ 已有成熟的原厂固件 root 方案
- ✅ 已有 FEL 模式进入方法验证
- ✅ 已有 NAND 分区布局文档
- ✅ 已有 UART 接口位置确认

这些社区验证过的信息可以直接作为 Project.Villy 的起点。

---

## 参考资源

- Dustcloud GitHub：https://github.com/dgiese/dustcloud
- Dustbuilder 使用指南：https://github.com/dgiese/dustbuilder-howto
- maker-tutorials（德语教程）：https://maker-tutorials.com/xiaomi-roborock-saugroboter-raspberry-pi-hack-root/
- Roboter-Forum（德语社区）：https://www.roboter-forum.com/
