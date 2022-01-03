"""
Plot results of benchmark. Need to run benchmark.py first to generate
the file benchmark_results.json.
"""
import json
from collections import defaultdict

import matplotlib.pyplot as plt


def groupby(values, keyfunc):
    """Group values by key returned by keyfunc."""
    groups = defaultdict(list)
    for value in values:
        key = keyfunc(value)
        groups[key].append(value)
    return groups


def main() -> None:
    """Plot benchmark results."""

    with open("benchmark_results.json", encoding="utf-8") as f:
        results = json.load(f)

    def keyfunc(result):
        return (result["zipfile"], result["threadcount"])

    for (zipfile, threadcount), results in groupby(results, keyfunc).items():

        results.sort(key=lambda result: result["filesize"])

        filesizes = []
        timings = []
        for result in results:
            filesizes.append(result["filesize"])
            timings.append(1000 * sum(result["timings"]) / len(result["timings"]))

        plt.loglog(
            filesizes,
            timings,
            label=f"{zipfile} - {threadcount} Thread{'s'[:threadcount-1]}",
        )

    plt.legend()
    plt.xlabel("File size [bytes]")
    plt.ylabel("Milliseconds to process a 10 MB zip file (lower is better)")
    plt.tight_layout()
    plt.savefig("benchmark.png")
    plt.show()


if __name__ == "__main__":
    main()
