#!/usr/bin/env python3

from bs4 import BeautifulSoup
import glob
import sys
import re
import json

import pdb


with open("currency-data.json", "r") as f:
    CURRENCY_TABLE = json.load(f)


def sek_to_usd(sek_amount, year):
    count = 0
    total = 0
    for conv in CURRENCY_TABLE:
        if conv["date"].startswith(str(year)):
            count += 1
            # Since the free version of Fixer.io only supports EUR as the base
            # currency, we have to first convert to EUR, then to USD
            eur_amount = sek_amount / conv["rates"]["SEK"]
            usd_amount = eur_amount * conv["rates"]["USD"]
            total += usd_amount
    assert count == 12
    # Now we have mid-month estimates for each month of the year, so return the
    # average
    return total / count


def main():
    for filepath in sorted(glob.glob(sys.argv[1] + "/*")):
        with open(filepath, "r") as f:
            print("Doing", filepath, file=sys.stderr)
            year = filepath.split("/")[-1][len("research-projects-"):-len(".html")]
            soup = BeautifulSoup(f, "lxml")
            for grant in soup_to_grants(soup, year):
                print(grant)


def soup_to_grants(soup, year):
    for item in soup.find_all("div", {"class": "list-item__content"}):
        project_title = item.find("h2").text
        amount_investigator = item.find("p", {"class": "list-item__post-title"}).text
        # Remove line separator character
        amount_investigator = amount_investigator.replace("\u2028", "")
        project_title = project_title.replace("\u2028", "")
        # Remove no-break space
        project_title = project_title.replace("\u00a0", " ")
        amount_investigator = amount_investigator.replace("\u00a0", " ")

        if ("Grant:" in amount_investigator and
            ("Principal Investigator:" in amount_investigator or
             "Principal investigator:" in amount_investigator)):
            parts = amount_investigator.split("\n")
            assert len(parts) == 2
            if parts[0].startswith("Grant:"):
                assert (parts[1].startswith("Principal Investigator:") or
                        parts[1].startswith("Principal investigator:"))
                amount_part = parts[0].strip()
                investigator_part = parts[1].strip()
            else:
                assert parts[1].startswith("Grant:")
                assert (parts[0].startswith("Principal Investigator:") or
                        parts[0].startswith("Principal investigator:"))
                amount_part = parts[1].strip()
                investigator_part = parts[0].strip()
        elif ("Beviljat anslag:" in amount_investigator and
              "Principal Investigator:" in amount_investigator):
            parts = amount_investigator.split("\n")
            assert parts[0].startswith("Beviljat anslag:")
            assert parts[1].startswith("Principal Investigator:")
            amount_part = parts[0]
            investigator_part = parts[1]
        elif "Final grant:" in amount_investigator:
            amount_part = amount_investigator.strip()
            investigator_part = ""
        elif "Grant:" in amount_investigator:
            amount_part = amount_investigator.strip()
            investigator_part = ""
        else:
            raise ValueError("We don't know this project format.")

        m = re.match(r"(?:Project|Projekt):[ ]?[“”]([^“”]+)[“”]", project_title)
        if m:
            project_title = m.group(1)
        else:
            m = re.match(r"Project: (.*)", project_title)
            if m:
                project_title = m.group(1)

        amount = None
        period = None
        m = re.search(r"SEK[ ]?([0-9 ,]+)", amount_part)
        if m:
            amount = float(m.group(1).replace(" ", "").replace(",", ""))
        elif amount_part == "Beviljat anslag: 35 131 000 kronor under fem år":
            amount = 35131000
            period = "five years"
        else:
            m = re.match(r"Grant: ([0-9 ,]+)", amount_part)
            if m:
                amount = float(m.group(1).replace(" ", "").replace(",", ""))

        assert amount is not None

        m = re.search(r"[0-9 ,]+ for a ([a-z]+)-year (?:project|projekt)", amount_part)
        if m:
            period = m.group(1) + " years"
        else:
            m = re.search(r"[0-9 ,]+ (?:kronor )?over ([a-z]+) years", amount_part)
            if m:
                period = m.group(1) + " years"
            else:
                m = re.match(r"(Grant|Final grant): SEK [0-9 ,]+(\.| in continuation grant\.| kronor)?$", amount_part)
                if m:
                    # There is no period information for this grant, so
                    # explicitly mark that
                    period = ""

        assert period is not None

        yield {"sek_amount": amount, "usd_amount": sek_to_usd(amount, int(year)),
               "project": project_title,
               "investigator": investigator_part,
               "focus_area": find_focus_area(item),
               "donation_date": year + "-01-01",
               "period": period}


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
