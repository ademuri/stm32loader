# Authors: Ivan A-R, Floris Lambrechts
# GitHub repository: https://github.com/florisla/stm32loader
#
# This file is part of stm32loader.
#
# stm32loader is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# stm32loader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with stm32loader; see the file LICENSE.  If not see
# <http://www.gnu.org/licenses/>.

"""Device-specific information and logic for STM32 microcontrollers."""

# Size of the Flash memory sector used when executing the Write Protect command.
# See ST AN2606.
WRITE_PROTECT_SECTOR_SIZE = {
    "default": 1024,
    "F0": 4 * 1024,
    "F1": 4 * 1024,
    "F3": 4 * 1024,
    "L0": 4 * 1024,
    "L4": 2 * 1024,
    "G0": 2 * 1024,
    "G4": 2 * 1024,
    "WL": 2 * 1024,
}


def get_write_protect_sectors(family, flash_size):
    """Return the list of sector indices to protect for the given flash size."""
    if family == "F4":
        # F405/415/407/417 and F42x/43x:
        # Bank 1:
        # Sectors 0-3: 16KB
        # Sector 4: 64KB
        # Sectors 5-11: 128KB
        # Total Bank 1: 1024KB, 12 sectors
        if flash_size <= 1024:
            if flash_size <= 64:
                sector_count = flash_size // 16
            elif flash_size <= 128:
                sector_count = 5
            else:
                sector_count = 5 + (flash_size - 128) // 128
        else:
            # Dual bank. Bank 2 (12-23) repeats the pattern.
            bank2_size = flash_size - 1024
            if bank2_size <= 64:
                bank2_sectors = bank2_size // 16
            elif bank2_size <= 128:
                bank2_sectors = 5
            else:
                bank2_sectors = 5 + (bank2_size - 128) // 128
            sector_count = 12 + bank2_sectors
            if sector_count > 24:
                sector_count = 24
        return list(range(sector_count))

    if family == "F7":
        # F74x/75x:
        # Sectors 0-3: 32KB
        # Sector 4: 128KB
        # Sectors 5-7: 256KB
        if flash_size <= 128:
            sector_count = flash_size // 32
        elif flash_size <= 256:
            sector_count = 5
        else:
            sector_count = 5 + (flash_size - 256) // 256
        return list(range(sector_count))

    if family == "H7":
        # H7: banks of 128KB sectors.
        return list(range((flash_size + 127) // 128))

    sector_size = WRITE_PROTECT_SECTOR_SIZE.get(family, WRITE_PROTECT_SECTOR_SIZE["default"])
    return list(range(flash_size * 1024 // sector_size))
