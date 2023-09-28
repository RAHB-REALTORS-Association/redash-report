from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

def send_email(sendgrid_api_key, from_email, to_emails, subject, content, xlsx_file):
    mail = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        plain_text_content=content
    )
    
    # Read the XLSX file in binary mode and encode it as Base64
    with open(xlsx_file, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()
    
    # Create an Attachment object for the XLSX file
    attachment = Attachment(
        file_content=FileContent(encoded_file),
        file_type=FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        file_name=FileName(xlsx_file),
        disposition=Disposition("attachment")
    )
    
    # Add the attachment to the mail
    mail.attachment = attachment
    
    # Create a SendGridAPIClient object and send the email
    client = SendGridAPIClient(sendgrid_api_key)
    response = client.send(mail)
    return response
