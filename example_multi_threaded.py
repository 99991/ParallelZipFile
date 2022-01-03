"""
Example for using ParallelZipFile to read multiple files in parallel using a
ThreadPool. With zipfile.ZipFile, this would crash instead.
"""
import zlib
from multiprocessing.pool import ThreadPool

from parallelzipfile import ParallelZipFile as ZipFile


def do_something_with_file(info):
    """Checking file integrity."""

    data = z.read(info.filename)

    computed_crc = zlib.crc32(data)

    assert computed_crc == info.CRC


with ZipFile("example.zip") as z:
    with ThreadPool() as pool:
        pool.map(do_something_with_file, z.infolist())
