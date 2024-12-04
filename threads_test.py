# thread_test.py
from sync_database import SyncDatabase
from threading import Thread


def reader(database, key):
    """
    handles reader applications
    :param database:
    :param key:
    :return:
    """
    print(f"Reading key {key}: {database.value_get(key)}")


def writer(database, key, value):
    """
    handles writer applications
    :param database:
    :param key:
    :param value:
    :return:
    """
    database.value_set(key, value)
    print(f"Writing key {key} with value {value}")


if __name__ == "__main__":
    db = SyncDatabase("db_file.pkl", mode="threads")

    writer_thread = Thread(target=writer, args=(db, "key1", "value1"))

    reader_threads = [Thread(target=reader, args=(db, "key1")) for _ in range(5)]

    writer_thread.start()
    writer_thread.join()

    for rt in reader_threads:
        rt.start()
    for rt in reader_threads:
        rt.join()
