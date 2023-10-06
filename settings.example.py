# Redash settings
redash_url = "https://www.example.com/redash"
api_key = "your_redash_api_key"
query_ids = [1, 2, 3]
titles = [
    "Title 1",
    "Title 2",
    "Title 3"
]

logo_url = "https://www.example.com/logo.png"
timestamp_format = "%Y-%m-%d"

# Email settings
sendgrid_api_key = "your_sendgrid_api_key"
from_email = "sender@example.com"
to_emails = ["recipient1@example.com", "recipient2@example.com"]
subject = "Summary Report for {{time_period}}"
content = "Please find attached the latest summary report for {{time_period}}."
template_path = "template.html"

# Scheduler settings
schedule_string = "0 0 * * *"  # Daily at midnight
mode = "xlsx"  # pdf, pdf-multi, xlsx, xlsx-multi