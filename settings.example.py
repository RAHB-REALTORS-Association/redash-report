# Redash settings
redash_url = "https://www.example.com/redash"
api_key = "your_redash_api_key"
query_ids = [1, 2, 3]  # Example query IDs
titles = [
    "Title 1",
    "Title 2",
    "Title 3"
]
logo_url = "https://www.example.com/logo.png"

# Email settings
sendgrid_api_key = "your_sendgrid_api_key"
from_email = "sender@example.com"
to_emails = ["recipient1@example.com", "recipient2@example.com"]
subject = "Summary Report for {{time_period}}"
content = "Please find attached the latest summary report for {{time_period}}."

# Schedule settings
day_of_month = "15"  # Example of day of the month
hour_of_day = 16  # time in UTC (noon EST)
