import schedule
import time
import io
import pandas as pd
from openpyxl import styles
import os
import argparse
from datetime import datetime
import requests
from send_email import send_email
import settings

headers = {
    "Authorization": f"Key {settings.api_key}"
}

def refresh_and_fetch_csv(query_id):    
    # Construct the refresh URL and send a POST request to refresh the query
    refresh_url = f"{settings.redash_url}/api/queries/{query_id}/refresh"
    response = requests.post(refresh_url, headers=headers)
    
    # Check the response status code
    if response.status_code == 200:
        print(f"Query {query_id} refreshed successfully.")
        
        # Construct the CSV URL and fetch the CSV data
        csv_url = f"{settings.redash_url}/api/queries/{query_id}/results.csv?api_key={settings.api_key}"
        response_csv = requests.get(csv_url, headers=headers)
        
        if response_csv.status_code == 200:
            csv_data = response_csv.content.decode('utf-8')
            data = pd.read_csv(io.StringIO(csv_data))
            return data
        else:
            print(f"Error fetching CSV for query {query_id}. Status code: {response_csv.status_code}")
    else:
        print(f"Error refreshing query {query_id}. Status code: {response.status_code}")
    return None


def job():
    # Check if today is the day of the month to run the job
    if datetime.today().day == settings.day_of_month:
        time_period = datetime.now().strftime(settings.timestamp_format)
        for query_id, title in zip(settings.query_ids, settings.titles):
            data = refresh_and_fetch_csv(query_id)
            if data is not None:
                # Convert to XLSX
                xlsx_file = f"{title} {time_period}.xlsx"
                with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
                    # Start writing CSV data from the third row
                    data.to_excel(writer, index=False, startrow=2)  # 0-indexed, so startrow=2 means the third row
                    
                    # Get the active worksheet
                    sheet = writer.sheets['Sheet1']
                    
                    # Set column widths
                    for column in sheet.columns:
                        max_length = max(len(str(cell.value)) for cell in column)
                        sheet.column_dimensions[column[0].column_letter].width = max_length
                    
                    # Define a cell style for bold and larger font
                    bold_large_font = styles.Font(bold=True, size=14)
                    
                    # Insert the title, time period, and total count in the specified cells
                    title_cell = sheet['B1']
                    title_cell.value = title
                    title_cell.font = bold_large_font
                    
                    date_cell = sheet['D1']
                    date_cell.value = time_period
                    date_cell.font = bold_large_font
                    
                    total_cell = sheet['F1']
                    total_cell.value = f"Total Count: {len(data)}"
                    total_cell.font = bold_large_font
                            
                # Send email with XLSX attached
                dynamic_subject = settings.subject.replace("{{time_period}}", time_period)
                dynamic_content = settings.content.replace("{{time_period}}", time_period)
                send_email(settings.sendgrid_api_key, settings.from_email, settings.to_emails, dynamic_subject, dynamic_content, xlsx_file)
                
                # Remove the XLSX file after sending the email
                os.remove(xlsx_file)


def main():
    parser = argparse.ArgumentParser(description='Run the job either according to schedule or immediately.')
    parser.add_argument('--now', action='store_true', help='Run the job immediately')
    
    args = parser.parse_args()
    
    if args.now:
        job()
    else:
        # Schedule the job to run every day at the specified hour, 
        # but the tasks inside the job will only execute if the day of the month matches the specified day in the settings.
        schedule.every().day.at(f"{settings.hour_of_day}:00").do(job)

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()
