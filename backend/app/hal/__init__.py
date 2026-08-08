# 硬件抽象层 (HAL)
#
# 此模块封装对底层硬件（GPIO、I2C、SPI、PWM）的访问，
# 提供统一的 Python 接口供 Flask API 调用。
#
# 子模块：
# - hal.gpio:    GPIO 控制器
# - hal.i2c:     I²C 总线
# - hal.sensors: 传感器接口实现
# - hal.motors:  电机控制接口实现
#
# 初期（阶段 2 完成前）使用 mock 实现进行 API 开发。
