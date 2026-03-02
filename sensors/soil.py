"""
MCP3008 ADC helper for capacitive soil moisture sensors.

Notes for Raspberry Pi deployment:
- Enable SPI: `sudo raspi-config` -> Interface Options -> SPI -> enable
- Install `spidev`: `pip3 install spidev`
"""
import logging
try:
    import spidev
except Exception:  # pragma: no cover - hardware
    spidev = None


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.spi = None
        if spidev:
            self.spi = spidev.SpiDev()
            self.spi.open(bus, device)
            self.spi.max_speed_hz = 1350000

    def read_channel(self, channel: int = 0) -> int:
        """Read raw ADC (0-1023)."""
        if not self.spi:
            logging.warning("spidev not available; returning 0")
            return 0
        # MCP3008 protocol: start bit, single/diff, channel
        cmd = 0b11 << 6 | (channel & 0x7) << 3
        resp = self.spi.xfer2([1, cmd, 0])
        value = ((resp[1] & 0x0F) << 8) | resp[2]
        return value

    def read_percent(self, channel: int = 0) -> float:
        raw = self.read_channel(channel)
        # convert to percent where 0 -> dry, 100 -> wet (device dependent)
        pct = max(0.0, min(100.0, (raw / 1023.0) * 100.0))
        return round(pct, 2)
