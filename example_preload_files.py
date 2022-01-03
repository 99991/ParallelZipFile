"""
This is an example on loading the ZipInfos from a zip file and then passing it
to a ZipFile object later. This is much faster if you need to process zip files
which contain a huuuuuge number of files with multiple processes.

ZipFiles can not be serialized due to the contained file object, which is why
Python's zipfile.ZipFile would have to re-read the file infos again and again
for every single process, but with parallelzipfile.ParallelZipFile, the first
file infos can be precomputed and serialized beforehand.
"""
from parallelzipfile import ParallelZipFile as ZipFile
from parallelzipfile import read_files

files = read_files("example.zip")

with ZipFile("example.zip", files=files) as z:
    for filename, info in files.items():
        if not info.is_dir():
            data = z.read(filename)
            print("File", filename, "contains", data)
