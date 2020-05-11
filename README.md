# Barotrauma-ID-Defragmenter
For when you have an item with the same key that has already been added.
## Prerequisites
- Python 3.8.0+
## Installation
- Download the source or clone the repo.
## Usage
Running `python defrag.py -h` produces:
```
usage: defrag.py [-h] files [files ...]

Defragment ID values in any number of .sub and .xml files. Designed to
work on precisely two files - a gamesession.xml and a .sub file from
an extracted .save file. YMMV with other options. Defragments all
files at once, so that they won't have any overlapping IDs.

positional arguments:
  files       The path to a file to defragment.

optional arguments:
  -h, --help  show this help message and exit
```
Some example usage:
- `python defrag.py gamesession.xml Dugong.sub`
It is not recommended to run `defrag` on only one of the two files in any given campaign save. This is because it might assign duplicate IDs, resulting in a crash and unusable files.