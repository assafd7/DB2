# thread_test.py
from sync_database import SyncDatabase
import multiprocessing


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
    db = SyncDatabase("db_file.pkl", mode="processes")

    writer_process = multiprocessing.Process(target=writer, args=(db, "key1", "hey"))
    reader_processes = [multiprocessing.Process(target=reader, args=(db, "key1")) for _ in range(5)]

    writer_process.start()
    writer_process.join()

    for rp in reader_processes:
        rp.start()
    for rp in reader_processes:
        rp.join()
