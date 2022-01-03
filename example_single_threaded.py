"""
Example for using ParallelZipFile to read a zip file. It is basically a drop-in
replacement for zipfile.ZipFile from the standard library.
"""
from parallelzipfile import ParallelZipFile as ZipFile

with ZipFile("example.zip") as z:
    for info in z.infolist():
        if not info.is_dir():
            data = z.read(info.filename)
            print("File", info.filename, "contains", data)
