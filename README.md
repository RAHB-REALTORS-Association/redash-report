# CSV to XLSX Report Generator

This project generates an XLSX report from CSV data obtained from Redash queries. The report is then emailed using SendGrid based on a predefined schedule. The queries in Redash are refreshed before fetching the CSV to ensure that the report contains the most up-to-date information.

## Requirements

- Python 3
- [Pandas](https://pandas.pydata.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) 
- [Requests](https://docs.python-requests.org/en/latest/)
- [Schedule](https://schedule.readthedocs.io/en/stable/)
- [SendGrid](https://sendgrid.com/)

You can install the required Python packages with pip:

```sh
pip install -r requirements.txt
```

## Configuration

You can configure the Redash base URL, API key, query IDs, report titles, logo URL, email settings, and schedule in `settings.py`. Ensure that the API key has sufficient permissions to refresh the queries and access the results.

## Usage

Run the main script with Python:

```sh
python main.py
```

You can also run the script immediately, bypassing the schedule, using the `--now` argument:

```sh
python main.py --now
```

The script will run indefinitely in the absence of the `--now` argument, generating and emailing a report according to the schedule specified in `settings.py`.

## Additional Information

- It is recommended to deploy this script in a stable environment where it can run uninterrupted, like a server or a cloud-based environment, to ensure consistent report generation and delivery.
- The time mentioned in `settings.py` for scheduling should be in UTC.

## License
This project is open source under the MIT license.
