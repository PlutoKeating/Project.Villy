# 2.7 Valetudo 生态调研

> Valetudo 是扫地机器人领域最重要的开源项目之一。本节分析其架构及其对 Project.Villy 的参考价值。

---

## Valetudo 是什么

**Valetudo**（拉丁语"健康"）是一个运行在扫地机器人上的**云替代服务**。它不是自定义固件，而是与厂商原始固件并行运行的"大脑寄生虫"——截获机器人与云端之间的通信，使一切在本地运行。

### 核心特性

| 特性 | 说明 |
|------|------|
| 完全离线 | 不需要任何云账户 |
| 隐私保护 | 所有数据留在本地 |
| 实时地图 | 浏览器内查看清扫路径 |
| Home Assistant | 原生 MQTT 集成 |
| Web UI | 内置管理界面 |
| 持续维护 | 2018 至今活跃开发 |

### 架构原理

```
┌─────────────────────────────────────┐
│            机器人内部                  │
│                                     │
│  厂商 App ──── Valetudo ──── 云端     │
│  (被拦截)       (MITM)      (被阻断)  │
│                  │                  │
│              MQTT ──── Home Assistant│
│              HTTP ──── Web UI        │
└─────────────────────────────────────┘
```

---

## 支持设备矩阵

Valetudo 目前支持以下设备系列（截至 2025年）：

| 厂商 | 系列 | 安装方法 |
|------|------|----------|
| Roborock | Gen1 (SDJQR01/02RR) | Dustbuilder + miioOTA |
| Roborock | Gen2 (S5 系列) | Dustbuilder |
| Roborock | S6/S7 系列 | UART 或 FEL |
| Dreame | L10/D9/Z10 系列 | Fastboot 或 UART |
| Dreame | X/L 高端系列 | UART 适配板 |
| Viomi | SE/V 系列 | 自定义方法 |
| Mijia | 1C/1T 系列 | 特定固件版本 |

---

## 对 Project.Villy 的参考价值

### 1. 硬件知识

Valetudo 社区积累了丰富的硬件信息：
- 各型号 PCB 照片和芯片清单
- UART 调试接口位置
- FEL 模式进入方法
- NAND Flash 分区布局

### 2. 协议知识

- miIO 协议：小米 IoT 设备通信协议
- 机器人状态机：清扫、回充、暂停等状态转换逻辑
- 传感器数据格式：LDS 激光数据、里程计、IMU

### 3. 软件架构

Valetudo 的模块化设计值得参考：
- **核心服务**：Go/Node.js 实现
- **MQTT 集成**：Home Assistant 生态对接
- **Web 前端**：Vue.js 仪表盘
- **REST API**：内部通信

### 4. 社区经验

- 数千用户的实机验证
- 大量踩坑和修复记录
- 丰富的安装教程和多语言文档

---

## Valetudo vs Project.Villy

| 维度 | Valetudo | Project.Villy |
|------|----------|--------------|
| 目标 | 去云端化 | 刷入完整 Linux |
| 方式 | 与厂商固件共存 | 完全替换固件 |
| 兼容性 | 需适配各型号 | 仅 SDJQR01RR |
| 复杂度 | 低（用户只需刷入） | 高（需内核开发） |
| 自由度 | 受限于原厂内核 | 完全自由 |

---

## 参考资源

- 官方网站：https://valetudo.cloud/
- GitHub：https://github.com/Hypfer/Valetudo
- 安装指南（Roborock）：https://valetudo.cloud/pages/installation/roborock/
- 支持设备列表：https://valetudo.cloud/pages/general/supported-robots.html
- 社区讨论：Home Assistant Community、Roboter-Forum、4PDA
- Hackaday 文章：https://hackaday.com/2026/07/21/open-source-vacuum-avoids-cloud/
