#
# This file is part of LiteX.
#
# This file is Copyright (c) 2018-2022 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from typing import Union, List

# Coloring Helpers ---------------------------------------------------------------------------------

def colorer(s, color="bright", enable=True):
    """Apply ANSI colors to a string."""
    header  = {
        "bright": "\x1b[1m",
        "green":  "\x1b[32m",
        "cyan":   "\x1b[36m",
        "red":    "\x1b[31m",
        "yellow": "\x1b[33m",
        "underline": "\x1b[4m"}[color]
    trailer = "\x1b[0m"
    return (header + str(s) + trailer) if enable else str(s)

# Byte Size Definitions ----------------------------------------------------------------------------

# Short.
KB = 1024
MB = KB * 1024
GB = MB * 1024

# Long.
KILOBYTE = 1024
MEGABYTE = KILOBYTE * 1024
GIGABYTE = MEGABYTE * 1024

# Bit/Bytes Reversing ------------------------------------------------------------------------------

def reverse_bits(s):
    """Return a signal with reversed bit order."""
    return s[::-1]

def reverse_bytes(s):
    """Return a signal with reversed byte order."""
    n = (len(s) + 7)//8
    return Cat(*[s[i*8:min((i + 1)*8, len(s))]
        for i in reversed(range(n))])


# DTS  ---------------------------------------------------------------------------------------------


def dts_constant(name: str, value: Union[int, str, List[int], List[str]] = None) -> str:
    """Returns a formatted dts string for the constant 'name'

    value can be None (default), int, str or a list of int or str.
    """
    if value is None:
        return f"{name};\n"
    elif isinstance(value, list):
        if all(isinstance(v, int) for v in value):
            of_value = "<" + " ".join(f"{v}" for v in value) + ">"
        elif all(isinstance(v, str) for v in value):
            of_value = ", ".join(f'"{v}"' for v in value)
        else:
            raise ValueError("All elements in the list must be of the same type (either all int or all str)")
        return f"{name} = {of_value};\n"
    else:
        of_value = f'"{value}"' if isinstance(value, str) else f"<{value}>"
        return f"{name} = {of_value};\n"
