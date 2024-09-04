import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage





# Hardcoded SMTP server settings
SMTP_SERVER = 'mail.spacecoinx.com'
SMTP_PORT = 587  # Port for TLS
SENDER_EMAIL = 'info@spacecoinx.com'
SENDER_PASSWORD = 'hoahdwedzjrllrxl'




def send_custom_email(recipient_email, sender_username, subject, is_html=True):
    """
    Function to send a welcome email with a logo and HTML content.
    
    :param recipient_email: Recipient's email address.
    :param sender_username: Sender's username (to personalize the email).
    :param subject: Subject of the email.
    :param is_html: Boolean indicating if the message is HTML (set to True by default).
    """

    # Create the email message
    msg = MIMEMultipart('related')
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Create the HTML body with inline CSS and the logo image
    html_content = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333333;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .content {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="cid:logo" alt="Logo" width="100%">
        </div>
        <div class="content">
            <h1>Welcome to Our Service, {sender_username}!</h1>
            <p>Dear {sender_username},</p>
            <p>Thank you for registering with us. We are excited to have you on board.</p>
            <p>We look forward to serving you!</p>
        </div>
        <div class="footer">
            &copy; 2024 Your Company. All rights reserved. SpaceCoinX
        </div>
    </body>
    </html>
    '''

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Attach the logo image
    with open('app/static/images/logo.png', 'rb') as img_file:
        logo = MIMEImage(img_file.read())
        logo.add_header('Content-ID', '<logo>')
        msg.attach(logo)

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
#send_custom_email('recipient@example.com', 'John Doe', 'Welcome to Our Service!')





recipient_email = 'musigwe@gmail.com'
sender_username = 'ugo'
subject = 'Welcome to Our Service!'
#otp = '123456'
#ogo_path = '/walletback/staticfiles/images/logo.png'  # Path to the logo image file on the server

#send_custom_email(recipient_email, sender_username, subject)