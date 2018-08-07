#!/usr/bin/env python3

from proc_research_projects import sek_to_usd, mysql_quote

def main():
    print("""insert into donations (donor, donee, donation_earmark, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, donor_cause_area_url, notes, amount_original_currency, original_currency, currency_conversion_date, currency_conversion_basis) values""")
    first = True
    with open("manual_data.tsv", "r") as f:
        for line in f:
            (grant_type, url, start_date, end_date, donee, donation_earmark,
             sek_amount, project, focus_area) = line[:-1].split("\t")
            if start_date:
                usd_amount = sek_to_usd(sek_amount, start_date[:len("YYYY")])
            else:
                usd_amount = sek_to_usd(sek_amount, 2016)  # TODO change?
            notes = []
            if project:
                notes.append("project: " + project)
            if start_date and end_date:
                notes.append(f"grant period: {start_date} to {end_date}")
            notes_str = "; ".join(notes)
            if notes_str:
                notes_str = notes_str[0].upper() + notes_str[1:]
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Knut and Alice Wallenberg Foundation"),  # donor
                mysql_quote(donee),  # donee
                mysql_quote(donation_earmark),  # donation_earmark
                str(usd_amount),  # amount
                mysql_quote(start_date if start_date else ""),  # donation_date
                mysql_quote("year" if start_date else ""),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(focus_area),  # cause_area
                mysql_quote(url),  # url
                mysql_quote(""),  # donor_cause_area_url
                mysql_quote(notes_str),  # notes
                str(sek_amount),  # amount_original_currency
                mysql_quote("SEK"),  # original_currency
                mysql_quote(grant["donation_date"]),  # currency_conversion_date
                mysql_quote("Fixer.io"),  # currency_conversion_basis
            ]) + ")")
            first = False
    print(";")



if __name__ == "__main__":
    main()
