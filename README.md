# Project.Villy

> **逆向你，改造你，让你重获新生。**
>
> Reverse engineering and secondary development of the Xiaomi Mi Robot Vacuum (SDJQR01RR) — transforming a first-generation robot vacuum into a Linux-powered, programmable, remote-controllable robot chassis.

---

## 🎯 Project Vision

I have an old **Xiaomi Mi Robot Vacuum (1st Gen, SDJQR01RR)** that's too outdated for daily use. Instead of letting it collect dust, I'm tearing it open to:

1. **Reverse-engineer** its hardware and embedded Linux system
2. **Replace / extend the firmware** with a modern Linux distribution
3. **Turn it into a programmable robot chassis** — controllable via WiFi, scriptable, sensor-accessible
4. **Document everything** so others can do the same

The end goal: a **fully open-source, Linux-running, remote-programmable robot platform** on affordable, accessible hardware.

---

## 🤖 Target Device

| Spec | Detail |
|------|--------|
| **Product** | 米家扫地机器人 / Mi Robot Vacuum |
| **Model** | **SDJQR01RR** (also listed as STYTJ01YM) |
| **OEM** | Roborock (石头科技) for Xiaomi |
| **Released** | August 2016 |
| **CPU** | Allwinner R16 — Quad-core ARM Cortex-A7 @ 1.2 GHz |
| **RAM** | 256 MB DDR3 |
| **Storage** | 512 MB NAND Flash |
| **WiFi** | Realtek RTL8189ETV (802.11 b/g/n, 2.4 GHz) |
| **OS** | Custom Linux (ARMv7, Buildroot-based) |
| **Battery** | 5200 mAh Li-ion (14.4 V) |

### Sensors & Actuators

| Component | Details |
|-----------|---------|
| **LDS** | Laser Distance Sensor (SLAM navigation, 360° scanning, ~6 m range) |
| **Ultrasonic Radar** | Forward obstacle detection |
| **Cliff Sensors** | 4× infrared drop sensors (front, left, right, rear) |
| **IMU** | 6-axis gyroscope + accelerometer |
| **Wheel Odometers** | 2× magnetic encoders on drive wheels |
| **Bumper** | Front collision detection (microswitch) |
| **Drive Wheels** | 2× BLDC motors with encoders |
| **Main Brush** | 1× BLDC motor |
| **Side Brush** | 1× BLDC motor |
| **Suction Fan** | 1× BLDC motor (variable speed) |

---

## 🗺️ Roadmap

### Phase 1 — Reconnaissance 🔍
- [ ] Open the device, photograph all PCBs
- [ ] Identify key chips: SoC, RAM, Flash, WiFi, motor drivers, sensor interfaces
- [ ] Locate UART / JTAG / USB debug pads
- [ ] Attempt serial console access (UART)
- [ ] Dump original firmware / boot logs

### Phase 2 — Understanding the Stock System 🧠
- [ ] Analyze boot process (bootloader, kernel, init system)
- [ ] Identify motor control protocol (PWM? UART to motor driver MCU?)
- [ ] Reverse-engineer sensor data streams (LDS, IMU, odometers, cliff, ultrasonic)
- [ ] Map GPIO pin assignments
- [ ] Understand the WiFi / cloud communication protocol

### Phase 3 — Rooting & Custom Firmware 🔓
- [ ] Achieve permanent root access (serial, firmware modification)
- [ ] Evaluate existing community projects (Valetudo, Dustcloud)
- [ ] Cross-compile a modern Linux kernel for Allwinner R16
- [ ] Build or adapt a minimal rootfs (Buildroot / Yocto / Debian armhf)
- [ ] Boot custom Linux from SD card or NAND

### Phase 4 — Robot Chassis Platform 🤖
- [ ] Write kernel drivers for all sensors and actuators
- [ ] Develop a hardware abstraction layer (HAL) — unified API for sensors + motors
- [ ] Implement WiFi-based remote control (WebSocket / HTTP API)
- [ ] ROS 2 integration (publish sensor data, subscribe to velocity commands)
- [ ] SLAM demo using the built-in LDS
- [ ] Autonomous navigation demo

### Phase 5 — Polish & Community 🚀
- [ ] 3D-printable accessory mounts (camera, Raspberry Pi, sensors)
- [ ] Web-based control dashboard
- [ ] Full documentation and build guide
- [ ] Publish everything as open source

---

## 📁 Repository Structure

```
Project.Villy/
├── README.md                   # This file
├── docs/                       # Documentation
│   ├── hardware/               # PCB photos, chip datasheets, pinouts
│   ├── firmware/               # Boot process, firmware analysis
│   └── build/                  # Build guides, cross-compilation notes
├── firmware/                   # Custom firmware / kernel patches
│   ├── kernel/                 # Linux kernel config and patches
│   └── rootfs/                 # Buildroot / Yocto configurations
├── hal/                        # Hardware Abstraction Layer
├── software/                   # Robot control software
│   ├── api/                    # HTTP / WebSocket control API
│   └── web/                    # Web-based control dashboard
├── ros2/                       # ROS 2 packages
├── 3d-models/                  # 3D-printable accessories
└── tools/                      # Debugging & development utilities
```

---

## 🔗 References & Community

- [Valetudo](https://github.com/Hypfer/Valetudo) — Cloud-free firmware for robot vacuums
- [Dustcloud](https://github.com/dgiese/dustcloud) — MITM proxy for Xiaomi robot vacuums
- [Allwinner R16 Datasheet](https://linux-sunxi.org/R16) — Linux-sunxi community wiki
- [Roborock Firmware Analysis](https://github.com/ghoost82/roborock-firmware) — Community firmware reverse engineering

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. The device is my personal property, no longer under warranty, and is being used as a hardware hacking platform. All work is done on my own device.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) file when added.

---

*"What's old can be new again — if you're willing to open it up and rewrite the rules."*
