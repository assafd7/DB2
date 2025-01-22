# thread_test_windows.py
from sync_database_windows import SyncDatabaseWindows
from threading import Thread


def reader(database, key):
    print(f"Reading key {key}: {database.value_get(key)}")


def writer(database, key, value):
    database.value_set(key, value)
    print(f"Writing key {key} with value {value}")


if __name__ == "__main__":
    db = SyncDatabaseWindows("db_file_windows.pkl")

    # Writer thread
    writer_thread = Thread(target=writer, args=(db, "key1", "value1"))

    # Reader threads
    reader_threads = [Thread(target=reader, args=(db, "key1")) for _ in range(5)]

    # Start threads
    writer_thread.start()
    writer_thread.join()

    for rt in reader_threads:
        rt.start()
    for rt in reader_threads:
        rt.join()

    db.close()
