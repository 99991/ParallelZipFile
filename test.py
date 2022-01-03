"""
Tests for parallelzipfile.py.
"""
import multiprocessing.pool
import os
import time
import zlib
from typing import Optional, Union

import parallelzipfile
from patch_zipfile import zipfile

AnyZipFileType = Union[zipfile.ZipFile, parallelzipfile.ParallelZipFile]


def verify_zipfile_crc32(
    z: AnyZipFileType, pool: multiprocessing.pool.ThreadPool
) -> None:
    """Check if CRC32 checksums for files in zip file are correct."""
    for filename, info in zip(z.namelist(), z.infolist()):
        assert filename == info.filename

    def check_file(info) -> None:
        data = z.read(info.filename)

        computed_crc = zlib.crc32(data)

        assert computed_crc == info.CRC

    pool.map(check_file, z.infolist())


def verify_zipfile_threadpool(z: AnyZipFileType) -> None:
    """Verify zip file content with both single and multithreaded."""
    start_time = time.perf_counter()
    pool = multiprocessing.pool.ThreadPool()
    verify_zipfile_crc32(z, pool)
    elapsed_time = time.perf_counter() - start_time
    print(f"Multi-threaded : {elapsed_time:.6f} seconds")

    start_time = time.perf_counter()
    pool = multiprocessing.pool.ThreadPool(1)
    verify_zipfile_crc32(z, pool)
    elapsed_time = time.perf_counter() - start_time
    print(f"Single-threaded: {elapsed_time:.6f} seconds")


per_process_zipfile: Optional[parallelzipfile.ParallelZipFile] = None


def check_file_processpool(info) -> None:
    """Check single zip file CRC32 checksum for process pool."""
    assert per_process_zipfile is not None
    data = per_process_zipfile.read(info.filename)

    computed_crc = zlib.crc32(data)

    assert computed_crc == info.CRC


def processpool_test(filename: str) -> None:
    """Test parallelzipfile with process pool."""
    start_time = time.perf_counter()
    files = parallelzipfile.read_files(filename)

    def initializer() -> None:
        global per_process_zipfile
        per_process_zipfile = parallelzipfile.ParallelZipFile(filename, files=files)

    with multiprocessing.pool.Pool(initializer=initializer) as pool:
        pool.map(check_file_processpool, files.values())

    elapsed_time = time.perf_counter() - start_time
    print(f"Multi-process: {elapsed_time:.6f} seconds")


def test() -> None:
    """Run tests for ZipFile and ParallelZipFile."""
    test_zipfile_name = "__test_parallelzipfile.zip"
    num_files = 10000
    filedata = os.urandom(1000)

    with zipfile.ZipFile(
        test_zipfile_name, "w", compression=zipfile.ZIP_STORED
    ) as z_write:
        for i in range(num_files):
            filename = f"{i}.txt"
            z_write.writestr(filename, filedata)

    for _ in range(1):
        print("parallelzipfile.ParallelZipFile")
        with parallelzipfile.ParallelZipFile(test_zipfile_name) as z_parallel:
            verify_zipfile_threadpool(z_parallel)

        print("zipfile.ZipFile")
        with zipfile.ZipFile(test_zipfile_name) as z:
            verify_zipfile_threadpool(z)
        print()

        print("parallelzipfile.ParallelZipFile (load ZipInfo once only)")
        processpool_test(test_zipfile_name)
        print()

    os.remove(test_zipfile_name)


if __name__ == "__main__":
    test()
