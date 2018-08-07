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
        amount_investigator = amount_investigator.replace("\u2028", "")  # Remove line separator character
        assert ("Grant:" in amount_investigator and "Principal Investigator:" in amount_investigator) or "Final grant:" in amount_investigator or ("Beviljat anslag" in amount_investigator and "Principal Investigator:" in amount_investigator) or "Grant:" in amount_investigator

        if "Grant:" in amount_investigator and ("Principal Investigator:" in amount_investigator or "Principal investigator:" in amount_investigator):
            parts = amount_investigator.split("\n")
            assert len(parts) == 2
            if parts[0].startswith("Grant:"):
                assert parts[1].startswith("Principal Investigator:") or parts[1].startswith("Principal investigator:")
                amount_part = parts[0].strip()
                investigator_part = parts[1].strip()
            else:
                assert parts[1].startswith("Grant:")
                assert parts[0].startswith("Principal Investigator:") or parts[0].startswith("Principal investigator:")
                amount_part = parts[1].strip()
                investigator_part = parts[0].strip()
            print(amount_part, investigator_part)
        elif "Beviljat anslag:" in amount_investigator and "Principal Investigator:" in amount_investigator:
            parts = amount_investigator.split("\n")
            assert parts[0].startswith("Beviljat anslag:")
            assert parts[1].startswith("Principal Investigator:")
            amount_part = parts[0]
            investigator_part = parts[1]
        elif "Final grant:" in amount_investigator:
            amount_part = amount_investigator.strip()
            investigator_part = ""
        elif "Grant:" in amount_investigator:
            pass
        else:
            raise ValueError("We don't know this project format.")

        # print(find_focus_area(item), project_title)


def find_focus_area(tag):
    """Go up and find the most recent h2."""
    # This depends on the specific div nesting used on the website, and might
    # break in the future
    tag = tag.parent.parent.parent
    while tag is not None and tag.name != "h2":
        tag = tag.previous_sibling
    if tag is None:
        return ""
    return tag.text.strip()


if __name__ == "__main__":
    main()
