# Knut and Alice Wallenberg Foundation

This is for the Donations List Website: https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/68

## How to get data and generate the SQL file

For research projects, download https://kaw.wallenberg.org/en/research-projects-2017
and the pages listed as "Earlier years" on that page.
Save in `data/` as `research-projects-YYYY.html` where `YYYY` is the year.

Get currency exchange rates by running `get_currency_data.py`.
You will need a Fixer.io API key stored in `apikey.txt`.

NOTE: if you need more recent years, be sure to change the year range
in `get_currency_data.py` before running the script.

```bash
./get_currency_data.py  # saves in currency-data.json
```

Now run `proc_research_projects.py`:

```bash
./proc_research_projects.py > out.sql
```

## License

CC0 for code and readme.
