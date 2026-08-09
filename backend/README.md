# Backend 后端服务

> 本模块负责在 SDJQR02RR 上运行的 Flask API 服务、硬件抽象层和认证体系。

## 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 语言 | Python 3.14+ | ARMv7 完整支持 |
| 框架 | Flask 3.x | 极轻量，< 5MB 内存开销 |
| 认证 | HMAC-SHA256 | 零外部依赖，硬件友好 |
| 实时通信 | Flask-Sock | WebSocket 遥测推送 |
| 测试 | pytest | 标准 Python 测试框架 |

## 目录结构

```
backend/
├── README.md              # 本文件
├── docs/
│   ├── api-reference.md   # API 端点完整文档
│   └── auth-scheme.md     # HMAC 认证方案设计
├── app/
│   ├── __init__.py         # Flask 工厂函数
│   ├── main.py             # 入口
│   ├── api/                # API 蓝图
│   │   ├── __init__.py
│   │   ├── status.py       # GET /api/v1/status
│   │   ├── sensors.py      # GET /api/v1/sensors
│   │   ├── motors.py       # POST /api/v1/motors
│   │   ├── system.py       # GET /api/v1/system
│   │   └── ws.py           # WebSocket 遥测
│   ├── auth/               # HMAC 认证
│   │   ├── __init__.py
│   │   ├── middleware.py    # Flask before_request 中间件
│   │   └── signer.py       # HMAC-SHA256 签名/验证
│   └── hal/                # 硬件抽象层
│       ├── __init__.py
│       ├── gpio.py          # GPIO 控制器
│       ├── i2c.py           # I²C 总线
│       ├── sensors/         # 传感器接口实现
│       └── motors/          # 电机控制接口实现
├── config/
│   ├── __init__.py
│   └── default.py           # 默认配置
├── requirements.txt
└── .gitignore
```

## 快速入口

| 文档 | 内容 |
|------|------|
| [API 参考](docs/api-reference.md) | 所有端点的请求/响应规范 |
| [认证方案](docs/auth-scheme.md) | HMAC 签名流程与安全设计 |

## 开发运行

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.main run --host 0.0.0.0 --port 5000
```

---

> 所有操作记录严格遵循 [AGENT.md](../../AGENT.md) 规范。
