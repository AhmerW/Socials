from gateway.data.email import EmailService, EMAIL_CONF

# default email service for account notifications
# verifications, security updates, etc...

email_service = EmailService(
    EMAIL_CONF,
    incl_name="Socials",
)
