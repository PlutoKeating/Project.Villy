# 组件树与数据流

## 组件树

```
App
├── Layout
│   ├── Navbar (导航栏)
│   └── <Outlet />
│
├── Dashboard (首页 /)
│   ├── StatusCard (状态卡片)
│   ├── BatteryGauge (电量)
│   ├── SensorPanel (传感器面板)
│   │   ├── SensorChart (IMU 实时图表)
│   │   └── LidarView (激光雷达可视化)
│   └── MotorStatus (电机状态)
│
├── Control (/control)
│   ├── Joystick (虚拟摇杆)
│   ├── MotorControl (电机滑块)
│   └── EmergencyStop (紧急停止按钮)
│
└── System (/system)
    ├── SystemInfo (CPU / RAM / Disk)
    ├── LogViewer (日志查看)
    └── AuthConfig (API Key 配置)
```

## 数据流

```
useTelemetry() hook
  │ WebSocket ws://<robot>:5000/api/v1/ws/telemetry
  │
  ├──→ Dashboard (实时传感器数据)
  │      └── Recharts 实时更新图表
  │
  └──→ Control (电机状态回显)
         └── MotorControl 滑块同步

signedFetch() (lib/api.ts)
  │ HTTP https://<robot>:5000/api/v1/*
  │ 自动附加 HMAC 签名头
  │
  ├──→ POST /motors (控制指令)
  ├──→ GET  /status
  └──→ GET  /system/info
```

## 响应式布局策略

- **Desktop (> 768px)**：左侧导航栏 + 中央内容区，三列仪表盘
- **Tablet (768px)**：顶部导航栏 + 两列仪表盘
- **Mobile (< 640px)**：底部导航栏 + 单列布局，摇杆全屏模式
