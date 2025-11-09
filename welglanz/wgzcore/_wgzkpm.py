"""WGZ Key Processing Module."""

from . import WINDOWS

from readchar import readkey

# Imports for POSIX compilant platforms.
if not WINDOWS:
    from sys import stdin

    from termios import tcsetattr, tcgetattr, TCSADRAIN

    from tty import setraw

    from os import read

    from select import select

    from time import time


# Timeout constants for POSIX compilant platforms.
POSIX_KR_TIMEOUT = 0x2 * .01

POSIX_KR_POTENTIAL_HANGING_LOOP_TIME = 0x5 * .1

# Welglanz's implementation of reading keys on POSIX compilant platforms.
def _wgz_readkey_posix() -> str:
    std_fd = stdin.fileno()

    old_attrs = tcgetattr(std_fd)

    try:
        setraw(std_fd)

        fbyte = read(std_fd, 0x1).decode('latin-1')

        if fbyte == '\x03':
            raise KeyboardInterrupt

        if fbyte == '\r':
            return '\n'

        if fbyte != '\x1b':
            return fbyte

        byte_seq = fbyte

        t_start = time()

        while True:
            if byte_seq and byte_seq[-1].isalpha():
                break

            rlist, _, _ = select([std_fd], [], [], POSIX_KR_TIMEOUT)

            if not rlist:
                break

            next_bytes = read(std_fd, 0x32).decode('latin-1')

            if not next_bytes:
                break

            byte_seq += next_bytes

            if time() - t_start > POSIX_KR_POTENTIAL_HANGING_LOOP_TIME:
                break

        return byte_seq
    finally:
        tcsetattr(std_fd, TCSADRAIN, old_attrs)

# Read a key regardless of a used platform.
def _wgz_pkm_readkey() -> str:
    if WINDOWS:
        return readkey()

    return _wgz_readkey_posix()
