"""PM2.5 Air Quality Sensor (PMSA003I / PM25) UART simple test.

Modeled after Adafruit's CircuitPython example, but configured for
Raspberry Pi UART RX/TX wiring.

Wiring (Raspberry Pi):
- Sensor VCC -> 5V (or 3V depending on your model; many PM25 boards use 5V)
- Sensor GND -> GND
- Sensor TX  -> Pi RX (GPIO 15 / UART RXD)
- Sensor RX  -> Pi TX (GPIO 14 / UART TXD)

Notes:
- Enable UART on the Pi (raspi-config -> Interface Options -> Serial):
  - Login shell over serial: Disable
  - Serial port hardware: Enable
- Many Raspberry Pi OS images expose the UART as /dev/serial0.

Dependencies (on the Pi):
- pip install adafruit-circuitpython-pm25 pyserial

Reference:
- https://learn.adafruit.com/pm25-air-quality-sensor/python-and-circuitpython
"""

import time


def _print_measurements(data: dict) -> None:
    # PM2.5 sensor returns a dict with keys like:
    # 'pm10 standard', 'pm25 standard', 'pm100 standard',
    # 'pm10 env', 'pm25 env', 'pm100 env',
    # plus particle counts.
    print("---------------------------------------")
    print(f"PM1.0 (standard):  {data['pm10 standard']}")
    print(f"PM2.5 (standard):  {data['pm25 standard']}")
    print(f"PM10  (standard):  {data['pm100 standard']}")
    print(f"PM1.0 (env):       {data['pm10 env']}")
    print(f"PM2.5 (env):       {data['pm25 env']}")
    print(f"PM10  (env):       {data['pm100 env']}")
    print("Particles > 0.3um / 0.1L air:", data["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", data["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", data["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", data["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", data["particles 50um"])
    print("Particles > 10 um / 0.1L air:", data["particles 100um"])


def main() -> None:
    try:
        import board
        import busio
        from adafruit_pm25.uart import PM25_UART
    except Exception as exc:  # pragma: no cover
        print("Missing Raspberry Pi / CircuitPython libraries.")
        print("Run this on a Raspberry Pi with:")
        print("  pip install adafruit-circuitpython-pm25 pyserial")
        print(f"Import error: {exc}")
        raise

    # Raspberry Pi UART pins (TX/RX). board.TX/board.RX map to the primary UART.
    # On many Pi OS setups, this corresponds to /dev/serial0.
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.25)

    # Create the PM25 sensor object. We set reset_pin=None because with UART wiring
    # you typically don't have a reset line connected.
    pm25 = PM25_UART(uart, reset_pin=None)

    print("PM2.5 UART simple test running... (Ctrl+C to stop)")

    while True:
        try:
            data = pm25.read()
        except RuntimeError:
            # Read errors are fairly common; keep going.
            print("Unable to read from sensor (retrying)...")
            time.sleep(1)
            continue

        print(time.ctime())
        _print_measurements(data)
        time.sleep(2)


if __name__ == "__main__":
    main()
