"""PM2.5 Air Quality Sensor (PMSA003I / PM25) UART simple test.

Modeled after Adafruit's CircuitPython example, but configured for
Raspberry Pi UART RX/TX wiring.

Wiring (Raspberry Pi):
- Sensor VCC -> 5V (or 3V depending on your model; many PM25 boards use 5V)
- Sensor GND -> GND
- Sensor TX  -> Pi RX (GPIO 15 / UART RXD)

One-way reading note:
- For basic reading, the Pi does NOT need to transmit to the sensor.
- You can leave Sensor RX unconnected (Pi TX not used).

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

import csv
import os
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


SERIAL_PORT = os.getenv("PM25_SERIAL_PORT", "/dev/serial0")
OUTPUT_CSV = "pm25_data.csv"
DURATION_S = 60  # fixed run time (seconds)
INTERVAL_S = 2   # seconds between successful reads


def main() -> None:
    try:
        import serial
        from adafruit_pm25.uart import PM25_UART
    except Exception as exc:  # pragma: no cover
        print("Missing libraries for PM2.5 UART reading.")
        print("Run this on a Raspberry Pi with:")
        print("  pip install adafruit-circuitpython-pm25 pyserial")
        print(f"Import error: {exc}")
        raise

    uart = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)

    # Create the PM25 sensor object. We set reset_pin=None because with UART wiring
    # you typically don't have a reset line connected.
    pm25 = PM25_UART(uart, reset_pin=None)  # type: ignore[arg-type]

    print(f"PM2.5 UART logging started. Duration={DURATION_S}s Interval={INTERVAL_S}s")
    print(f"Serial port: {SERIAL_PORT}")
    print(f"Output CSV:  {OUTPUT_CSV}")

    start_ts = time.time()
    end_ts = start_ts + max(0, int(DURATION_S))
    reads = 0

    # Write CSV with a metadata line first, then a header row.
    with open(OUTPUT_CSV, "w", newline="") as f:
        f.write(
            "# meta," +
            f"start_epoch={int(start_ts)}," +
            f"duration_s={int(DURATION_S)}," +
            f"interval_s={int(INTERVAL_S)}," +
            f"port={SERIAL_PORT}\n"
        )
        writer = csv.writer(f)
        writer.writerow(
            [
                "t_s",
                "pm25_standard",
                "pm25_env",
                "pm10_standard",
                "pm100_standard",
                "particles_03um",
                "particles_05um",
                "particles_10um",
                "particles_25um",
                "particles_50um",
                "particles_100um",
            ]
        )

        try:
            while time.time() < end_ts:
                try:
                    data = pm25.read()
                except RuntimeError:
                    print("Unable to read from sensor (retrying)...")
                    time.sleep(0.5)
                    continue

                now = time.time()
                t_s = int(now - start_ts)
                print(f"t={t_s}s")
                _print_measurements(data)

                writer.writerow(
                    [
                        t_s,
                        data.get("pm25 standard"),
                        data.get("pm25 env"),
                        data.get("pm10 standard"),
                        data.get("pm100 standard"),
                        data.get("particles 03um"),
                        data.get("particles 05um"),
                        data.get("particles 10um"),
                        data.get("particles 25um"),
                        data.get("particles 50um"),
                        data.get("particles 100um"),
                    ]
                )
                f.flush()
                reads += 1

                time.sleep(max(0, int(INTERVAL_S)))
        finally:
            try:
                uart.close()
            except Exception:
                pass

    print(f"Done. Logged {reads} readings to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
