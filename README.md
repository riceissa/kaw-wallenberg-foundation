# Knut and Alice Wallenberg Foundation

This is for the Donations List Website: https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/68

## How to get data and generate the SQL file

### Currency stuff

Currency data is stored in the repo at `currency-data.json`.
If all the dates you need for currency conversions are already
in the JSON file, then you don't need to get new currency data,
so you can skip this part.

Get currency exchange rates by running `get_currency_data.py`.
You will need a Fixer.io API key stored in `apikey.txt`.

NOTE: if you need more recent years, be sure to change the year range
in `get_currency_data.py` before running the script.

WARNING: running the script overwrites `currency-data.json`.
This is actually okay most of the time since that file is
tracked by Git, so the old file is automatically kept around.
However, if you have uncommitted changes to the file that
you would like to keep, make sure to copy the file first.

```bash
./get_currency_data.py  # saves in currency-data.json
```

### Research projects

For research projects, download https://kaw.wallenberg.org/en/research-projects-2017
and the pages listed as "Earlier years" on that page.
Save in `data/` as `research-projects-YYYY.html` where `YYYY` is the year.

Now run `proc_research_projects.py`:

```bash
./proc_research_projects.py data > out.sql
```

### Other grants

These are the grants listed on the following pages:

* https://kaw.wallenberg.org/en/strategic-grants
* https://kaw.wallenberg.org/en/earlier-grants
* https://kaw.wallenberg.org/en/infrastructure-national-importance-2012-2014

Since the data format for these is messy and not standardized,
you will need to manually collect the data and store it in
`manual_data.tsv`. The format for the TSV is tab-separated values
and no quoting or escaping of any kind.

Once the data is collected, run `proc_manual_data.py`:

```bash
# Append output to out.sql
./proc_manual_data.py >> out.sql
```

## License

CC0 for code and readme.
