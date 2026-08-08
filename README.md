# 🤖 Project.Villy

> **小米初代扫地机器人（SDJQR01RR）逆向工程与二次开发 —— 让它重获新生，变身可编程 Linux 机器人底盘。**

---

## 这是什么？

我有一台 **小米扫地机器人 1 代（型号 SDJQR01RR，石头科技 2016 年出品）**，因为太老旧已经无法正常服役。与其让它吃灰，不如拆开来大干一场：

- 逆向分析它的硬件和嵌入式 Linux 系统
- 刷入现代 Linux 发行版，替换原厂固件
- 把一台「扫地机」改造成 **可通过 WiFi 遥控、可编程的机器人底盘**
- 完整记录过程，让其他人也能复现

> 一句话：**让退役的扫地机器人，变成你的下一台机器人开发平台。**

---

## 目标硬件

| 规格 | 详情 |
|------|------|
| **产品** | 米家扫地机器人 / Mi Robot Vacuum |
| **型号** | SDJQR01RR（亦标为 STYTJ01YM） |
| **代工厂** | 石头科技 Roborock |
| **发布时间** | 2016 年 8 月 |
| **CPU** | 全志 Allwinner R16，四核 ARM Cortex-A7 @ 1.2GHz |
| **内存** | 256 MB DDR3 |
| **存储** | 512 MB NAND Flash |
| **WiFi** | Realtek RTL8189ETV（802.11 b/g/n，2.4GHz） |
| **电池** | 5200 mAh 锂电（14.4V） |
| **系统** | 定制 Linux（ARMv7，Buildroot 系） |

**传感器与执行器一览：**

| 组件 | 说明 |
|------|------|
| LDS 激光雷达 | 360° 激光测距，SLAM 导航核心 |
| 超声波雷达 | 前方障碍物检测 |
| 悬崖传感器 | 4 组红外传感器 |
| IMU | 六轴陀螺仪 + 加速度计 |
| 里程计 | 2 组驱动轮磁编码器 |
| 碰撞传感器 | 前撞微动开关 |
| 驱动轮 ×2 | BLDC 电机 + 编码器 |
| 主刷 / 边刷 / 风机 | 各 1 个 BLDC 电机 |

---

## 路线图

### 第一阶段 —— 侦察
- [ ] 拆机，拍摄所有 PCB 高清照片
- [ ] 识别关键芯片：SoC、RAM、Flash、WiFi、电机驱动、传感器接口
- [ ] 定位 UART / JTAG / USB 调试触点
- [ ] 尝试串口终端接入
- [ ] 导出原始固件 / 启动日志

### 第二阶段 —— 理解原厂系统
- [ ] 分析启动流程（bootloader → kernel → init）
- [ ] 查明电机控制协议（PWM？串口？）
- [ ] 逆向传感器数据流（LDS、IMU、里程计、悬崖、超声波）
- [ ] 映射 GPIO 引脚分配
- [ ] 理解 WiFi / 云端通信协议

### 第三阶段 —— 获取 Root 权限 & 定制固件
- [ ] 实现持久 root 访问
- [ ] 评估社区项目（Valetudo、Dustcloud）
- [ ] 为 Allwinner R16 交叉编译现代 Linux 内核
- [ ] 构建 / 适配最小 rootfs（Buildroot / Yocto / Debian armhf）
- [ ] 从 SD 卡或 NAND 启动自定义 Linux

### 第四阶段 —— 机器人底盘平台
- [ ] 编写传感器和电机驱动的内核驱动
- [ ] 开发硬件抽象层（HAL）—— 统一的传感器 + 电机 API
- [ ] 实现 WiFi 遥控（WebSocket / HTTP API）
- [ ] ROS 2 集成（发布传感器数据，订阅速度指令）
- [ ] 基于 LDS 的 SLAM 演示
- [ ] 自主导航演示

### 第五阶段 —— 打磨 & 社区共享
- [ ] 3D 打印扩展支架（摄像头、树莓派等）
- [ ] 网页版控制面板
- [ ] 完整文档和构建指南
- [ ] 全部开源发布

---

## 目录结构

```
Project.Villy/
├── README.md                # 本文件
├── docs/                    # 文档
│   ├── hardware/            # PCB 照片、芯片数据手册、引脚定义
│   ├── firmware/            # 启动流程、固件分析
│   └── build/               # 构建指南、交叉编译笔记
├── firmware/                # 定制固件 / 内核补丁
│   ├── kernel/              # Linux 内核配置与补丁
│   └── rootfs/              # Buildroot / Yocto 配置
├── hal/                     # 硬件抽象层
├── software/                # 机器人控制软件
│   ├── api/                 # HTTP / WebSocket 控制 API
│   └── web/                 # 网页控制面板
├── ros2/                    # ROS 2 包
├── 3d-models/               # 3D 打印模型
└── tools/                   # 调试与开发工具
```

---

## 社区参考

- [Valetudo](https://github.com/Hypfer/Valetudo) —— 扫地机器人去云端固件
- [Dustcloud](https://github.com/dgiese/dustcloud) —— 小米扫地机器人中间人代理
- [Allwinner R16 @ linux-sunxi](https://linux-sunxi.org/R16) —— 全志 R16 社区文档
- [Roborock Firmware Analysis](https://github.com/ghoost82/roborock-firmware) —— 石头扫地机固件分析

---

## 免责声明

本项目仅供 **学习与研究**。所用设备为本人自有财产，已过保修期。所有工作均在自有设备上完成。

---

> *"旧物新生，始于拆开它、改写规则的那一刻。"*
