"""Unit tests for the devices module."""

from stm32loader import devices


def test_get_write_protect_sectors_f1():
    # F1 has 4KB write protect sectors.
    # 64KB / 4KB = 16 sectors.
    assert devices.get_write_protect_sectors("F1", 64) == list(range(16))


def test_get_write_protect_sectors_f4_512k():
    # F4: 0-3: 16KB (64KB), 4: 64KB (128KB), 5-11: 128KB (1024KB)
    # 512KB means 4 sectors (64KB) + 1 sector (64KB) + (512-128)/128 = 3 sectors (384KB)
    # total 8 sectors
    assert devices.get_write_protect_sectors("F4", 512) == list(range(8))


def test_get_write_protect_sectors_f4_1024k():
    # 1024KB = 12 sectors
    assert devices.get_write_protect_sectors("F4", 1024) == list(range(12))


def test_get_write_protect_sectors_f4_2048k():
    # 2048KB = 24 sectors
    assert devices.get_write_protect_sectors("F4", 2048) == list(range(24))


def test_get_write_protect_sectors_f7_1024k():
    # F7: 0-3: 32KB (128KB), 4: 128KB (256KB), 5-7: 256KB (1024KB)
    # 1024KB = 8 sectors
    assert devices.get_write_protect_sectors("F7", 1024) == list(range(8))
