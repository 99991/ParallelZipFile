"""Benchmark to compare performance of ZipFile and ParallelZipFile."""
import json
import os
import time
import zlib
from multiprocessing.pool import ThreadPool

import parallelzipfile
from patch_zipfile import zipfile


def main():
    """Run benchmark."""

    # 10 MB
    totalsize = 10 ** 7
    zip_filename = "__test_parallelzipfile.zip"
    filesizes = [int(100 * (1000 ** 0.1) ** i) for i in range(11)]
    results = []

    for filesize in filesizes:
        # Compute number of files such that total size is approximately 10 MB
        # given a certain file size.
        filecount = totalsize // filesize
        filedata = os.urandom(filesize)

        # Generate zip file with filecount files of size filesize.
        with zipfile.ZipFile(
            zip_filename, "w", compression=zipfile.ZIP_DEFLATED
        ) as z_write:
            for i in range(filecount):
                z_write.writestr(f"{i}.txt", filedata)

        # Test two different ZipFile implementations
        for ZipFile in [zipfile.ZipFile, parallelzipfile.ParallelZipFile]:
            # Test various numbers of threads
            for threadcount in [1, 2, 4, 8]:
                # Run 10 times to get a reasonable average
                timings = []
                for _ in range(10):
                    # Check that decompressed content is correct
                    def check(info):
                        data = z.read(info.filename)
                        computed_crc = zlib.crc32(data)
                        assert computed_crc == info.CRC

                    # Begin Benchmark
                    start_time = time.perf_counter()

                    with ThreadPool(threadcount) as pool:
                        with ZipFile(zip_filename) as z:
                            pool.map(check, z.infolist())

                    # End benchmark
                    elapsed_time = time.perf_counter() - start_time
                    timings.append(elapsed_time)

                results.append(
                    {
                        "filesize": filesize,
                        "filecount": filecount,
                        "zipfile": ZipFile.__name__,
                        "threadcount": threadcount,
                        "timings": timings,
                    }
                )
                print(results[-1])

    # Save results
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # Cleanup
    os.remove(zip_filename)


if __name__ == "__main__":
    main()
