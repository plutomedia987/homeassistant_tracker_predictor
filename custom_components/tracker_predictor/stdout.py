import io
import os
import sys
import tempfile
from contextlib import contextmanager

import ctypes

# use_errno parameter is optional, because I'm not checking errno anyway.
libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)


class FILE(ctypes.Structure):
    pass


FILE_p = ctypes.POINTER(FILE)

# Alternatively, we can just use:
# FILE_p = ctypes.c_void_p

# These variables, defined inside the C library, are readonly.
cstdin = FILE_p.in_dll(libc, "stdin")
cstdout = FILE_p.in_dll(libc, "stdout")
cstderr = FILE_p.in_dll(libc, "stderr")

# C function to disable buffering.
csetbuf = libc.setbuf
csetbuf.argtypes = (FILE_p, ctypes.c_char_p)
csetbuf.restype = None

# C function to flush the C library buffer.
cfflush = libc.fflush
cfflush.argtypes = (FILE_p,)
cfflush.restype = ctypes.c_int


@contextmanager
def capture_c_stdout(encoding="utf8"):
    # Flushing, it's a good practice.
    sys.stdout.flush()
    cfflush(cstdout)

    # We need to use a actual file because we need the file descriptor number.
    with tempfile.TemporaryFile(buffering=0) as temp:
        # Saving a copy of the original stdout.
        prev_sys_stdout = sys.stdout
        prev_stdout_fd = os.dup(1)
        os.close(1)

        # Duplicating the temporary file fd into the stdout fd.
        # In other words, replacing the stdout.
        os.dup2(temp.fileno(), 1)

        # Replacing sys.stdout for Python code.
        #
        # IPython Notebook version of sys.stdout is actually an
        # in-memory OutStream, so it does not have a file descriptor.
        # We need to replace sys.stdout so that interleaved Python
        # and C output gets captured in the correct order.
        #
        # We enable line_buffering to force a flush after each line.
        # And write_through to force all data to be passed through the
        # wrapper directly into the binary temporary file.
        temp_wrapper = io.TextIOWrapper(
            temp, encoding=encoding, line_buffering=True, write_through=True
        )
        sys.stdout = temp_wrapper

        # Disabling buffering of C stdout.
        csetbuf(cstdout, None)

        yield

        # Must flush to clear the C library buffer.
        cfflush(cstdout)

        # Restoring stdout.
        os.dup2(prev_stdout_fd, 1)
        os.close(prev_stdout_fd)
        sys.stdout = prev_sys_stdout

        # Printing the captured output.
        temp_wrapper.seek(0)
        print(temp_wrapper.read(), end="")
