# 2.7 Valetudo 生态调研

> Valetudo 支持 CRL200S 平台的多种机型。本节分析其对 Project.Villy 的参考价值。

---

## Valetudo 的 CRL200S 支持

CRL200S (3irobotix) 是 Valetudo 官方支持的平台之一，覆盖以下机型：

| 品牌 | 型号 | 设备 ID |
|------|------|---------|
| Xiaomi | Mijia 1S | dreame.vacuum.* |
| Xiaomi | Vacuum-Mop P | viomi.vacuum.v8 |
| Viomi | V2, V7 | viomi.vacuum.v7 |
| Cecotec | Conga 3290 | — |
| Proscenic | M6 Pro | — |

### 安装方法

CRL200S 的 root 方法远比其他平台简单：

1. **ADB over Micro USB** — 免拆机、免焊接
2. 使用 `Hypfer/valetudo-crl200s-root` 工具
3. 通过 Dustbuilder 生成定制固件

详见: https://valetudo.cloud/pages/installation/dreame/

---

## Valetudo vs Project.Villy

| 维度 | Valetudo | Project.Villy |
|------|----------|--------------|
| 目标 | 去云端化 | 完整 Linux 替换 |
| 方式 | 与厂商固件共存 | 完全替换固件 |
| 依赖 | 依赖原厂内核和驱动 | 主线 Linux + 自研驱动 |
| 复杂度 | 低 (ADB + 脚本) | 高 (内核开发、DTS) |
| 自由度 | 受限于原厂系统 | 完全自由 |

---

## 对 Project.Villy 的参考价值

1. **调试入口**: ADB root 方法可直接用于 CRL200S 的初始访问
2. **协议知识**: miIO 协议、机器人状态机
3. **社区经验**: 大量用户的实机验证
4. **硬件信息**: Valetudo 社区积累的 PCB 照片和拆机文档

---

## 参考资源

- Valetudo 官网: https://valetudo.cloud/
- Dreame 安装指南: https://valetudo.cloud/pages/installation/dreame/
- CRL200S root 工具: https://github.com/Hypfer/valetudo-crl200s-root
- Dustbuilder: https://builder.dontvacuum.me/
