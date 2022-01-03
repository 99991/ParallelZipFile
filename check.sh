#!/usr/bin/env bash
isort *.py
black *.py
mypy --strict parallelzipfile.py
pylint --disable=W0511,C0301,C0103,R0913,R0903,R0914,R1732,R1705,W0612,W0603,W0212,W0640 *.py
