import os

# Redash settings
redash_url = os.environ.get('REDASH_URL', "https://www.example.com/redash")
api_key = os.environ.get('API_KEY', "your_redash_api_key")
query_ids = os.environ.get('QUERY_IDS', "1,2,3").split(',')  # Converts "1,2,3" to [1, 2, 3]
query_ids = [int(qid) for qid in query_ids]  # Convert string IDs to integers
titles = os.environ.get('TITLES', "Title 1,Title 2,Title 3").split(',')  # Converts "Title 1,Title 2,Title 3" to ['Title 1', 'Title 2', 'Title 3']

logo_url = os.environ.get('LOGO_URL', "https://www.example.com/logo.png")
timestamp_format = os.environ.get('TIMESTAMP_FORMAT', "%Y-%m-%d")

# Email settings
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY', "your_sendgrid_api_key")
from_email = os.environ.get('FROM_EMAIL', "sender@example.com")
to_emails = os.environ.get('TO_EMAILS', "recipient1@example.com,recipient2@example.com").split(',')  # Converts "recipient1@example.com,recipient2@example.com" to ['recipient1@example.com', 'recipient2@example.com']
subject = os.environ.get('SUBJECT', "Summary Report for {{time_period}}")
content = os.environ.get('CONTENT', "Please find attached the latest summary report for {{time_period}}.")

# Schedule settings
day_of_month = int(os.environ.get('DAY_OF_MONTH', 15))  # Convert string to integer
hour_of_day = int(os.environ.get('HOUR_OF_DAY', 16))  # Convert string to integer
