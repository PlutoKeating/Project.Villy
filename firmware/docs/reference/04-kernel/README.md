# 2.4 内核配置与设备树

> 为 SDJQR02RR 定制 Linux 内核，编写适配硬件的设备树（DTS）。

---

## 内核配置策略

### 最小内核配置

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- sunxi_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```

### 必须启用的内核选项

```ini
# Allwinner SoC 支持
CONFIG_ARCH_SUNXI=y
CONFIG_MACH_SUN8I=y
CONFIG_SUN8I_A33_PLATFORM=y

# 存储
CONFIG_MTD=y
CONFIG_MTD_NAND=y
CONFIG_MTD_NAND_SUNXI=y
CONFIG_SQUASHFS=y

# 网络
CONFIG_WLAN=y
CONFIG_RTL8189ES=m    # WiFi

# 传感器 I/O
CONFIG_I2C=y
CONFIG_I2C_MV64XXX=y  # Allwinner I2C
CONFIG_SPI=y
CONFIG_SPI_SUN6I=y    # Allwinner SPI

# GPIO
CONFIG_GPIO_SYSFS=y
CONFIG_PINCTRL_SUN8I_A33=y

# PWM
CONFIG_PWM=y
CONFIG_PWM_SUNXI=y

# USB
CONFIG_USB_MUSB_HDRC=y
CONFIG_USB_MUSB_SUNXI=y

# IMU
CONFIG_INV_MPU6050_IIO=m
```

---

## 设备树（Device Tree）

### 设备树结构

```
sun8i-a33.dtsi                # SoC 级别定义（主线提供）
  └── sun8i-a33-sdjqr02rr.dts # 板级定义（需自行编写）
```

### 基础 DTS 模板

```dts
/dts-v1/;
#include "sun8i-a33.dtsi"
#include "sunxi-common-regulators.dtsi"

/ {
    model = "Xiaomi Mi Robot Vacuum SDJQR02RR";
    compatible = "xiaomi,sdjqr02rr", "allwinner,sun8i-a33", "allwinner,sun8i-a33";

    chosen {
        stdout-path = "serial0:115200n8";
    };

    /* WiFi 电源控制 */
    wifi_pwrseq: wifi_pwrseq {
        compatible = "mmc-pwrseq-simple";
        reset-gpios = <&pio 7 5 GPIO_ACTIVE_LOW>; /* PH5 */
    };
};

/* UART0: 调试串口（PB 引脚） */
&uart0 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart0_pb_pins>;
    status = "okay";
};

/* UART1: STM32 电机 MCU */
&uart1 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart1_pg_pins>;
    status = "okay";
};

/* I2C0: MPU-6050 IMU */
&i2c0 {
    status = "okay";
    mpu6050@68 {
        compatible = "invensense,mpu6050";
        reg = <0x68>;
        interrupt-parent = <&pio>;
        interrupts = <1 0 IRQ_TYPE_EDGE_RISING>; /* PB0 */
    };
};

/* MMC1: SDIO WiFi (RTL8189ETV) */
&mmc1 {
    pinctrl-names = "default";
    pinctrl-0 = <&mmc1_pg_pins>;
    vmmc-supply = <&reg_dcdc1>;
    mmc-pwrseq = <&wifi_pwrseq>;
    bus-width = <4>;
    non-removable;
    status = "okay";
};

/* NAND */
&nfc {
    status = "okay";
    nand@0 {
        reg = <0>;
        allwinner,rb = <0>;
        nand-ecc-mode = "hw";
        nand-on-flash-bbt;
    };
};

/* PWM: 电机控制 */
&pwm {
    pinctrl-names = "default";
    pinctrl-0 = <&pwm0_pin>, <&pwm1_pin>;
    status = "okay";
};
```

### 编译 DTS

```bash
# 编译
dtc -I dts -O dtb -o sun8i-a33-sdjqr02rr.dtb sun8i-a33-sdjqr02rr.dts

# 反编译（验证）
dtc -I dtb -O dts sun8i-a33-sdjqr02rr.dtb > verify.dts

# 或通过内核构建系统
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- dtbs
```

---

## GPIO sysfs 调试

```bash
# 导出 GPIO
echo 0 > /sys/class/gpio/export     # PA0
echo 32 > /sys/class/gpio/export    # PB0

# 设置方向
echo out > /sys/class/gpio/gpio0/direction
echo in > /sys/class/gpio/gpio32/direction

# 读写
echo 1 > /sys/class/gpio/gpio0/value
cat /sys/class/gpio/gpio32/value
```

---

## 参考资源

- 内核 sunxi DTS 目录：`arch/arm/boot/dts/allwinner/`
- pinctrl 绑定：`Documentation/devicetree/bindings/pinctrl/allwinner,sunxi-pinctrl.txt`
- sunxi GPIO 外部中断：https://linux-sunxi.org/External_interrupts
- Banana Pi M2 Magic DTS 参考（R16 板）：主线内核 `sun8i-a33-bananapi-m2m.dts`
