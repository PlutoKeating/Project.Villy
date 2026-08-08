# 3.1 HAL 硬件抽象层设计

> 设计轻量、可测试、可桥接的硬件抽象层。

---

## 设计原则

### 1. 接口先于实现

先定义抽象接口，再实现具体硬件驱动：

```python
from abc import ABC, abstractmethod

class MotorInterface(ABC):
    """驱动轮电机抽象接口"""
    
    @abstractmethod
    def set_speed(self, left: float, right: float) -> None:
        """设置左右轮速度 (-100 到 100)"""
        ...
    
    @abstractmethod
    def stop(self) -> None:
        """紧急停止"""
        ...
    
    @abstractmethod
    def get_odometry(self) -> tuple[int, int]:
        """获取编码器计数 (left, right)"""
        ...

class SensorInterface(ABC):
    """传感器抽象接口"""
    
    @abstractmethod
    def read(self) -> dict:
        """读取传感器数据, 返回标准化字典"""
        ...
    
    @abstractmethod
    def calibrate(self) -> bool:
        """校准传感器"""
        ...
```

### 2. Mock 实现支持离线开发

```python
class MockMotor(MotorInterface):
    """Mock 实现, 用于无硬件时的开发和测试"""
    def set_speed(self, left, right):
        print(f"[MOCK] Motors: L={left} R={right}")
    def stop(self):
        print("[MOCK] Motors: STOP")
    def get_odometry(self):
        return (0, 0)
```

---

## 硬件访问模式

### GPIO (sysfs)

```python
class GpioController:
    """通过 sysfs 控制 GPIO"""
    
    def __init__(self, pin: int):
        self.pin = pin
        self._export()
    
    def _export(self):
        with open('/sys/class/gpio/export', 'w') as f:
            f.write(str(self.pin))
    
    def set_direction(self, direction: str):
        with open(f'/sys/class/gpio/gpio{self.pin}/direction', 'w') as f:
            f.write(direction)
    
    def set_value(self, value: int):
        with open(f'/sys/class/gpio/gpio{self.pin}/value', 'w') as f:
            f.write(str(value))
    
    def get_value(self) -> int:
        with open(f'/sys/class/gpio/gpio{self.pin}/value') as f:
            return int(f.read().strip())
```

### I2C (smbus2)

```python
from smbus2 import SMBus

class I2CDevice:
    def __init__(self, bus: int, address: int):
        self.bus = SMBus(bus)
        self.address = address
    
    def read_byte(self, reg: int) -> int:
        return self.bus.read_byte_data(self.address, reg)
    
    def write_byte(self, reg: int, value: int):
        self.bus.write_byte_data(self.address, reg, value)
    
    def read_block(self, reg: int, length: int) -> list:
        return self.bus.read_i2c_block_data(self.address, reg, length)
```

### PWM (sysfs)

```python
class PwmController:
    def __init__(self, chip: int, channel: int):
        path = f'/sys/class/pwm/pwmchip{chip}'
        self._export(path, channel)
        self.path = f'{path}/pwm{channel}'
    
    def _export(self, chip_path, channel):
        with open(f'{chip_path}/export', 'w') as f:
            f.write(str(channel))
    
    def set_period(self, period_ns: int):
        with open(f'{self.path}/period', 'w') as f:
            f.write(str(period_ns))
    
    def set_duty_cycle(self, duty_ns: int):
        with open(f'{self.path}/duty_cycle', 'w') as f:
            f.write(str(duty_ns))
    
    def enable(self):
        with open(f'{self.path}/enable', 'w') as f:
            f.write('1')
```

---

## 社区参考: Python 嵌入式 HAL

| 项目 | 说明 |
|------|------|
| **gpiozero** | Raspberry Pi 的 Python GPIO 库, API 设计优雅 |
| **Adafruit Blinka** | 跨平台 GPIO 抽象库 |
| **smbus2** | 纯 Python I2C/SMBus 库 |
| **pyserial** | Python 串口通信 (UART) |
| **python-periphery** | 通用 GPIO/I2C/SPI/MMIO Python 库, 最适合嵌入式 |

**推荐**: `python-periphery` 是最适合 Villy 的选择 -- 不依赖特定 SBC, 支持 sysfs GPIO, I2C, SPI, MMIO 和串口。

---

## HAL 子模块设计

```
backend/app/hal/
├── __init__.py          # HAL 工厂函数
├── interfaces.py        # 抽象接口定义
├── gpio.py              # GPIO 控制器
├── i2c.py               # I2C 总线
├── pwm.py               # PWM 控制器
├── uart.py              # UART 通信
├── sensors/
│   ├── lidar.py         # LDS 激光雷达
│   ├── imu.py           # MPU-6050
│   ├── ultrasonic.py    # 超声波
│   └── cliff.py         # 悬崖传感器
├── motors/
│   ├── wheels.py        # 驱动轮
│   ├── brush.py         # 主刷/边刷
│   └── fan.py           # 风机
└── mock/                # Mock 实现
    ├── sensors.py
    └── motors.py
```
