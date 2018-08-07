#!/usr/bin/env python3

from bs4 import BeautifulSoup
import glob
import sys

import pdb


def main():
    for filepath in sorted(glob.glob(sys.argv[1] + "/*")):
        with open(filepath, "r") as f:
            print("Doing", filepath, file=sys.stderr)
            soup = BeautifulSoup(f, "lxml")
            soup_to_grants(soup)


def soup_to_grants(soup):
    for item in soup.find_all("div", {"class": "list-item__content"}):
        project_title = item.find("h2").text
        amount_investigator = item.find("p", {"class": "list-item__post-title"}).text
        assert ("Grant:" in amount_investigator and "Principal Investigator:" in amount_investigator) or "Final grant:" in amount_investigator or ("Beviljat anslag" in amount_investigator and "Principal Investigator:" in amount_investigator) or "Grant:" in amount_investigator

        print(find_title(item), project_title)


def find_title(tag):
    """Go up and find the most recent h2."""
    # pdb.set_trace()
    tag = tag.parent.parent.parent
    while tag is not None and tag.name != "h2":
        tag = tag.previous_sibling
    if tag is None:
        return ""
    return tag.text.strip()


if __name__ == "__main__":
    main()
