# API 端点参考

> 所有端点前缀：`/api/v1`
> 所有请求需携带 HMAC 签名头（详见 `auth-scheme.md`）

---

## 状态

### `GET /status`

机器人运行状态摘要。

**响应：**
```json
{
  "status": "ok",
  "uptime": 3600,
  "battery": {"voltage": 14.2, "percentage": 85},
  "mode": "idle",
  "errors": []
}
```

---

## 传感器

### `GET /sensors`

获取最近一次所有传感器读数快照。

**响应：**
```json
{
  "timestamp": 1754678423,
  "lidar": {"rpm": 300, "ranges": [0.5, 0.52, ...]},
  "imu": {"accel": {"x": 0.01, "y": 0.02, "z": 9.81}, "gyro": {"x": 0, "y": 0, "z": 0}},
  "odometry": {"left": 1234, "right": 1235},
  "ultrasonic": {"distance": 1.2},
  "cliff": {"front": false, "left": false, "right": false, "rear": false}
}
```

### `GET /sensors/<name>`

获取指定传感器实时数据。`name` 取值：`lidar`, `imu`, `odometry`, `ultrasonic`, `cliff`。

---

## 电机控制

### `POST /motors`

发送电机控制指令。

**请求体：**
```json
{
  "left_motor": 50,
  "right_motor": 50,
  "main_brush": 0,
  "side_brush": 0,
  "fan": 0
}
```

值范围：`-100`（全速反转）到 `100`（全速正转），`0` 停止。

**响应：**
```json
{"result": "ok", "timestamp": 1754678423}
```

### `POST /motors/stop`

紧急停止所有电机。

---

## 系统

### `GET /system/info`

系统信息。

**响应：**
```json
{
  "hostname": "villy",
  "kernel": "Linux 6.x.y",
  "distro": "Debian 13",
  "cpu_usage": 12.5,
  "memory": {"total": 256, "used": 64, "free": 192},
  "disk": {"total": 512, "used": 128, "free": 384}
}
```

---

## WebSocket

### `WS /ws/telemetry`

实时遥测推送流。连接后持续推送传感器数据帧。

**推送帧格式：**
```json
{
  "type": "sensors|motors|system",
  "timestamp": 1754678423,
  "data": { ... }
}
```

---

*待实现后更新。*
