# database.py
import ctypes
from ctypes.wintypes import HANDLE, DWORD
import pickle

# Constants for CreateFile
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_ALWAYS = 4
CREATE_ALWAYS = 2
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2

# Load kernel32 functions
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


class DatabaseWindows:
    def __init__(self, filename):
        self.filename = filename
        self.handle = self._open_file(filename)
        self.data = {}
        self._load_from_file()

    @staticmethod
    def _open_file(filename):
        handle = kernel32.CreateFileW(
            ctypes.c_wchar_p(filename),
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_ALWAYS,
            0,
            None
        )
        if handle == HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        return handle

    def _load_from_file(self):
        try:
            self.data = self._read_file()
        except EOFError:
            self.data = {}

    def _write_file(self):
        serialized_data = pickle.dumps(self.data)
        kernel32.SetFilePointer(self.handle, 0, None, 0)
        bytes_written = DWORD()
        success = kernel32.WriteFile(
            self.handle,
            ctypes.c_char_p(serialized_data),
            len(serialized_data),
            ctypes.byref(bytes_written),
            None
        )
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())

    def _read_file(self):
        file_size = kernel32.GetFileSize(self.handle, None)
        if file_size == 0:
            return {}
        buffer = ctypes.create_string_buffer(file_size)
        bytes_read = DWORD()
        success = kernel32.ReadFile(
            self.handle,
            buffer,
            file_size,
            ctypes.byref(bytes_read),
            None
        )
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        return pickle.loads(buffer[:bytes_read.value])

    def value_set(self, key, value):
        self.data[key] = value
        self._write_file()
        return True

    def value_get(self, key):
        return self.data.get(key, None)

    def value_delete(self, key):
        value = self.data.pop(key, None)
        self._write_file()
        return value

    def close(self):
        kernel32.CloseHandle(self.handle)
