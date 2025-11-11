import os
from agents import function_tool
from init_agent import initAgent
import mailtrap as mt

@function_tool
def send_email(subject: str, html_body: str):
    """ Send an email with the given subject and HTML body """

    email = os.environ.get("EMAIL_FROM")
    client = mt.MailtrapClient(token=os.environ.get("MAILTRAP_API_KEY"))

    # Create mail object
    mail = mt.Mail(
        sender=mt.Address(email="info@everscending.org"),
        to=[mt.Address(email=email)],
        subject=subject,
        html=html_body,
        content_type="text/html",
    )

    response = client.send(mail)
    print("Email response", response)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = initAgent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email]
)
