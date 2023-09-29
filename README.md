[![Continuous Integration](https://github.com/RAHB-REALTORS-Association/redash-report/actions/workflows/python-app.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/redash-report/actions/workflows/python-app.yml)
[![Docker Image](https://github.com/RAHB-REALTORS-Association/redash-report/actions/workflows/docker-image.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/redash-report/actions/workflows/docker-image.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 📊 Redash Reports 📈

This project generates .XLSX or .PDF reports from CSV data obtained from Redash queries. The report is then emailed using SendGrid based on a predefined schedule. The queries in Redash are refreshed before fetching the CSV to ensure that the report contains the most up-to-date information.

## Table of Contents
- [✅ Requirements](#-requirements)
- [🛠️ Configuration](#configuration)
- [🧑‍💻 Usage](#-usage)
- [🐳 Running with Docker](#-running-with-docker)
- [🌐 Community](#-community)
  - [Contributing 👥](#contributing-)
  - [Reporting Bugs 🐛](#reporting-bugs-)
- [📄 License](#-license)

## ✅ Requirements

- Python 3
- [Pandas](https://pandas.pydata.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Schedule](https://schedule.readthedocs.io/en/stable/)
- [SendGrid](https://sendgrid.com/)

You can install the required Python packages with pip:

```bash
pip install -r requirements.txt
```

## 🛠️ Configuration
You can configure the Redash base URL, API key, query IDs, report titles, logo URL, email settings, and the report generation schedule through environment variables or the `settings.py` file. Ensure that the API key has sufficient permissions to refresh the queries and access the results. 

Additionally, you can set the report mode (XSLX or PDF) through command-line arguments or the `settings.py` file. The schedule should be specified in the cron format in the `settings.py` file.

## 🧑‍💻 Usage
Run the main script with Python:

```bash
python main.py --mode [xlsx|pdf] --now
```

- `--mode`: Sets the report mode to use (XSLX or PDF).
- `--now`: Run the report immediately, bypassing the schedule.

### Examples
Run the script immediately, generating a PDF report:

```bash
python main.py --mode pdf --now
```

The script will run indefinitely in the absence of the `--now` argument, generating, and emailing a report according to the schedule specified in the `settings.py`.

## 🐳 Running with Docker

To get started, you first need to pull the Docker image from the GitHub Container Registry. You can do this by running the following command in your terminal:

```bash
docker pull ghcr.io/rahb-realtors-association/redash-report:latest
```

Set environment variables as needed and run with the following command:

```bash
docker run ghcr.io/rahb-realtors-association/redash-report:latest --mode [xlsx|pdf] --now
```

Alternatively, you can use a `settings.py` file to configure your environment. Download the `settings.example.py` and save it as `settings.py`. Modify as needed and run with the following command:

```bash
docker run -v /path/to/your/settings.py:/app/settings.py ghcr.io/rahb-realtors-association/redash-report:latest --mode [xlsx|pdf] --now
```

## 🌐 Community

### Contributing 👥

Contributions, whether in the form of features, code improvements, or bug reports, are always welcome! Please refer to the contributing guidelines and the code of conduct.

[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/redash-report/compare)

### Reporting Bugs 🐛

Found a bug? Open an issue detailing the bug and how it can be reproduced. Please include system information, logs, and any other information that could be helpful in fixing the bug.

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/redash-report/issues/new/choose)

## 📄 License
This project is open source under the MIT license. See the [LICENSE](LICENSE) file for more info. 📜