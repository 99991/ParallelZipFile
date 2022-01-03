This is an mmap-based ParallelZipFile implementation since Python's ZipFile is currently (2022-01-01) not thread safe.

## Gotchas:

* Only reading is supported. Writing zip files is not supported.
* Only a very limited subset of the zip file specification is implemented ("good enough" for my use cases).
* There probably are bugs. Use at your own risk.

## Benchmark

![Benchmark](https://raw.githubusercontent.com/99991/ParallelZipFile/main/benchmark.png)

This plot shows how long it takes to process a 10 MB zip file containing files of varying size with 1, 2, 4 or 8 threads using ZipFile or ParallelZipFile.

* For very small files, single threaded performance is higher than multi-threaded performance, but multi-threaded performance is higher for medium to large files.
* ParallelZipFile is faster than ZipFile with almost any number of threads. The difference decreases with larger files.
* The optimal number of threads depends on the file size.
* This is a logarithmic plot, so differences are larger than they might appear at first glance.

#### Benchmark details

Benchmarks were run on an Intel Core i5-10300H processor (4 cores) on Xubuntu 20.04. Results are the average of ten runs (median looks about the same). All data is "hot", i.e. cached in RAM.

#### TODO

Find out why single threaded performance is higher than multi-threaded performance for small files. The following points have been investigated so far:

* Congestion due to dict lookup of ZipInfo objects - roughly the same performance when using a cloned dict for each thread.
* Reading of End-of-Central-Directory header not parallel - only makes up a very small percentage of total running time.
* Using processes instead of threads - much slower due to overhead of starting a new process.
* Thread scheduling overhead - processing multiple files at once with each thread performs about the same.
