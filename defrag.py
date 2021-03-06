import argparse
import gzip
from os import path
import re
import xml.etree.ElementTree as ET

contained_pattern = r"(?:(?<=,)|^){VALUE}(?:(?=,)|$)"
attributes = ["ID", "w", "linked", "contained", "gap", "ladders"]

parser = argparse.ArgumentParser(
    description="""Defragment ID values in any number of .sub and .xml files.
    
    Designed to work on precisely two files - a gamesession.xml and a
    .sub file from an extracted .save file. YMMV with other options.
    
    Defragments all files at once, so that they won't have any overlapping
    IDs."""
)
parser.add_argument("files", nargs="+", type=str, help="The path to a file to defragment.")


def load_sub(sub_filepath):
    with gzip.open(sub_filepath, "rb") as sub:
        return sub.read()


def write_sub(sub_filepath, stuff):
    with gzip.open(sub_filepath, "wb+") as sub:
        sub.write(stuff)


if __name__ == "__main__":
    args = parser.parse_args()
    data = dict()
    ids = set()
    for f in args.files:
        if not path.isfile(f):
            continue

        ext = path.splitext(f)[-1].lower()
        if ext == ".sub":
            data[f] = ET.fromstring(load_sub(f))
        elif ext == ".xml":
            data[f] = ET.parse(f, parser=ET.XMLParser(encoding="utf-8")).getroot()

    for tree in data.values():
        for node in tree.iter():
            for attribute in attributes:
                if value := node.attrib.get(attribute):
                    if matches := re.findall(
                        contained_pattern.format(VALUE=r"\d+"), value
                    ):
                        for match in matches:
                            ids.add(int(match))

            cont = True
            count = 0
            while cont:
                if linkedto := node.attrib.get(f"linkedto{count}"):
                    ids.add(int(linkedto))
                    count += 1
                else:
                    cont = False

    ids = list(ids)
    ids.sort()

    id_map = dict()
    for new, old in enumerate(ids):
        id_map[old] = new + 1

    for tree in data.values():
        for node in tree.iter():
            for attribute in attributes:
                if value := node.attrib.get(attribute):
                    if matches := re.findall(
                        contained_pattern.format(VALUE=r"\d+"), value
                    ):
                        for match in matches:
                            node.set(
                                attribute,
                                value := re.sub(
                                    contained_pattern.format(VALUE=str(match)),
                                    str(id_map[int(match)]),
                                    value,
                                ),
                            )
            cont = True
            count = 0
            while cont:
                if linkedto := node.attrib.get(f"linkedto{count}"):
                    node.set(f"linkedto{count}", str(id_map[int(linkedto)]))
                    count += 1
                else:
                    cont = False

    for f, x in data.items():
        ext = path.splitext(f)[-1].lower()
        if ext == ".sub":
            write_sub(f, ET.tostring(x))
        else:
            with open(f, "wb+") as sub:
                sub.write(ET.tostring(x))
