# sync_database_windows.py
from database_windows import DatabaseWindows
import ctypes

WAIT_OBJECT_0 = 0x00000000
INFINITE = 0xFFFFFFFF

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


class SyncDatabaseWindows(DatabaseWindows):
    def __init__(self, filename):
        super().__init__(filename)
        self.read_semaphore = self._create_semaphore(10)
        self.write_mutex = self._create_mutex()

    @staticmethod
    def _create_semaphore(max_count):
        semaphore = kernel32.CreateSemaphoreW(None, max_count, max_count, None)
        if not semaphore:
            raise ctypes.WinError(ctypes.get_last_error())
        return semaphore

    @staticmethod
    def _create_mutex():
        mutex = kernel32.CreateMutexW(None, False, None)
        if not mutex:
            raise ctypes.WinError(ctypes.get_last_error())
        return mutex

    def start_read(self):
        result = kernel32.WaitForSingleObject(self.read_semaphore, INFINITE)
        if result != WAIT_OBJECT_0:
            raise ctypes.WinError(ctypes.get_last_error())

    def end_read(self):
        kernel32.ReleaseSemaphore(self.read_semaphore, 1, None)

    def start_write(self):
        result = kernel32.WaitForSingleObject(self.write_mutex, INFINITE)
        if result != WAIT_OBJECT_0:
            raise ctypes.WinError(ctypes.get_last_error())

    def end_write(self):
        kernel32.ReleaseMutex(self.write_mutex)

    def value_set(self, key, value):
        self.start_write()
        try:
            return super().value_set(key, value)
        finally:
            self.end_write()

    def value_get(self, key):
        self.start_read()
        try:
            return super().value_get(key)
        finally:
            self.end_read()

    def value_delete(self, key):
        self.start_write()
        try:
            return super().value_delete(key)
        finally:
            self.end_write()
