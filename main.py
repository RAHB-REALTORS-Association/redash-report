import argparse
import io
from datetime import datetime, timedelta
import os
import time

import pandas as pd
import requests
import schedule

import settings
from create_pdf import create_pdf_report, create_pdf_report_multi
from create_xlsx import create_xlsx_report, create_xlsx_report_multi
from send_email import send_email


def refresh_and_fetch_csv(query_id):
    headers = {
        "Authorization": f"Key {settings.api_key}"
    }

    # Construct the refresh URL and send a POST request to refresh the query
    refresh_url = f"{settings.redash_url}/api/queries/{query_id}/refresh"
    response = requests.post(refresh_url, headers=headers)
    
    # Check the response status code
    if response.status_code == 200:
        print(f"Query {query_id} refreshed successfully.")

        # Introduce a 15-second delay before fetching the CSV
        time.sleep(15)
        
        # Construct the CSV URL and fetch the CSV data
        csv_url = f"{settings.redash_url}/api/queries/{query_id}/results.csv?api_key={settings.api_key}"
        response_csv = requests.get(csv_url, headers=headers)
        
        if response_csv.status_code == 200:
            # Convert the CSV data into a Pandas DataFrame
            csv_data = response_csv.content.decode('utf-8')
            data = pd.read_csv(io.StringIO(csv_data))
            return data
        else:
            print(f"Error fetching CSV for query {query_id}. Status code: {response_csv.status_code}")
    else:
        print(f"Error refreshing query {query_id}. Status code: {response.status_code}")
    return None


def run_report(mode='xlsx'):
    dataframes = []
    titles = []

    # Get the start and end dates for the report
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Adjust the timedelta as needed
    time_period = datetime.now().strftime(settings.timestamp_format)

    # Refresh and fetch the CSV data for each query
    for query_id, title in zip(settings.query_ids, settings.titles):
        data = refresh_and_fetch_csv(query_id)
        if data is not None:
            dataframes.append(data)
            titles.append(title)
    
    if dataframes:
        output_path = f"Report_{time_period}.{'pdf' if mode == 'pdf' else 'xlsx'}"
        # Replace the {{time_period}} placeholder in the subject and content
        dynamic_subject = settings.subject.replace("{{time_period}}", time_period)
        dynamic_content = settings.content.replace("{{time_period}}", time_period)

        if mode == 'xlsx':
            # Create the Excel file and send it as an email attachment
            report_files = create_xlsx_report(dataframes, titles, time_period)
            send_email(settings.sendgrid_api_key, settings.from_email, settings.to_emails, dynamic_subject, dynamic_content, report_files)
            try:
                for file in report_files:
                    os.remove(file)
            except Exception as e:
                print(f"Error in deleting the file: {e}")

        elif mode == 'xlsx-multi':
            # Create the Excel files and send them as a email attachments
            report_files = create_xlsx_report_multi(dataframes, titles, time_period)
            send_email(settings.sendgrid_api_key, settings.from_email, settings.to_emails, dynamic_subject, dynamic_content, report_files)
            try:
                for file in report_files:
                    os.remove(file)
            except Exception as e:
                print(f"Error in deleting the file: {e}")

        elif mode == 'pdf':
            # Create the PDF file and send it as an email attachment
            report_files = create_pdf_report(dataframes, titles, output_path, settings.logo_url, start_date, end_date)
            send_email(settings.sendgrid_api_key, settings.from_email, settings.to_emails, dynamic_subject, dynamic_content, report_files)
            try:
                for file in report_files:
                    os.remove(file)
            except Exception as e:
                print(f"Error in deleting the file: {e}")

        elif mode == 'pdf-multi':
            # Create the PDF files and send them as a email attachments
            report_files = create_pdf_report_multi(dataframes, titles, settings.logo_url, start_date, end_date)
            send_email(settings.sendgrid_api_key, settings.from_email, settings.to_emails, dynamic_subject, dynamic_content, report_files)
            try:
                for file in report_files:
                    os.remove(file)
            except Exception as e:
                print(f"Error in deleting the file: {e}")


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Generate and send Redash reports.')
    
    # Add command-line arguments
    parser.add_argument('--mode', type=str, choices=['xlsx', 'xlsx-multi', 'pdf', 'pdf-multi'], default=settings.mode, help='Report mode: xlsx, xlsx-multi, pdf, or pdf-multi.')
    parser.add_argument('--now', action='store_true', help='Run the report immediately.')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # If --now argument is passed, run the report immediately
    if args.now:
        run_report(args.mode)
        return
    
    # Schedule the report based on the schedule_string from settings
    schedule.every().cron(settings.schedule_string).do(run_report, args.mode) # pylint: disable=no-member
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
