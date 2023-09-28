# CSV Report Generator

This project generates a PDF report based on CSV data from specified URLs. The report is generated weekly at a specified time, and then emailed using SendGrid.

## Requirements

- Python 3
- [ReportLab](https://www.reportlab.com/opensource/)
- [Pandas](https://pandas.pydata.org/)
- [Schedule](https://schedule.readthedocs.io/en/stable/)
- [SendGrid](https://sendgrid.com/)

You can install the required Python packages with pip:

```sh
pip install -r requirements.txt
```

## Configuration
You can configure the CSV data sources, report titles, logo URL, email settings, and schedule in `settings.py`.

## Usage
Run the main script with Python:

```sh
python main.py
```

The script will run indefinitely, generating and emailing a report according to the schedule specified in `settings.py`.

## License
This project is open source under the MIT license.
