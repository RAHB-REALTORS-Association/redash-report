from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, Personalization
import base64
import mimetypes


def send_email(sendgrid_api_key, from_email, to_emails, subject, content, files):
    mail = Mail(
        from_email=from_email,
        subject=subject,
        plain_text_content=content
    )
    
    # Create a Personalization object and add all the recipients to it
    personalization = Personalization()
    for to_email in to_emails:
        personalization.add_to(to_email)
    mail.add_personalization(personalization)
    
    # Handle multiple attachments
    for file in files:
        with open(file, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode()

        # Dynamically determine the file_type based on the file extension
        file_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'

        attachment = Attachment(
            file_content=FileContent(encoded_file),
            file_type=FileType(file_type),  # Set the file_type dynamically
            file_name=FileName(file),
            disposition=Disposition("attachment")
        )

        mail.add_attachment(attachment)
    
    client = SendGridAPIClient(sendgrid_api_key)
    response = client.send(mail)
    return response
